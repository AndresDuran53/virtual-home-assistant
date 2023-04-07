import requests
from datetime import datetime,timedelta,timezone
from libs.general_devices import GeneralDevice
from libs.calendar import Calendar
from libs.sensor import Sensor
from libs.binary_sensor import BinarySensor
from libs.person import Person,Greeting

class HomeAssistantServices:
    def __init__(self, url, token, people, calendars, list_sensors, binary_sensors, general_devices):
        self.url = url
        self.token = token
        self.filling_list_devices(people, calendars, list_sensors, binary_sensors, general_devices,)
        self.last_data=self.requests_general_data()

    def filling_list_devices(self, people, list_calendar, list_sensors, list_binary_sensors, list_general_devices):
        self.person_status = []
        for person in people:
            self.person_status.append(Person(person["id"],person["name"]))

        self.important_calendars = []
        for calendar_aux in list_calendar:
            self.important_calendars.append(Calendar(calendar_aux["id"],calendar_aux["owner"]))

        self.sensors = []
        for sensor_aux in list_sensors:
            self.sensors.append(Sensor(sensor_aux["id"],sensor_aux["name"]))

        self.binary_sensors = []
        for binary_sensor_aux in list_binary_sensors:
            self.binary_sensors.append(BinarySensor(binary_sensor_aux["id"],binary_sensor_aux["name"],binary_sensor_aux["offValue"],binary_sensor_aux["onValue"]))

        self.general_devices = []
        for general_device_aux in list_general_devices:
            self.general_devices.append(GeneralDevice(general_device_aux["id"],general_device_aux["name"],ignoring_states = general_device_aux["ignoringStates"]))

    def update_data(self):
        self.last_data=self.requests_general_data()
    
    def get_people_information(self, data = None):
        if(data == None): data = self.last_data
        self.update_person_state(data)
        return self.person_status
    
    def get_calendars_events(self):
        self.update_events_by_calendar()
        return self.important_calendars
    
    def get_sensors(self,data = None):
        if(data == None): data = self.last_data
        self.update_binary_sensors(data)
        self.update_sensors(data)
        return self.sensors + self.binary_sensors
    
    def get_general_devices(self,data=None):
        if(data == None): data = self.last_data
        self.update_general_devices(data)
        return self.general_devices

    def requests_general_data(self):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(self.url+"/states", headers=headers)
        data = response.json()
        return data
    
    def requests_calendar_events(self,calendar_id,future_days=3):
        now = datetime.now()
        actual_time_string = now.strftime("%Y-%m-%d")
        future_time = (now + timedelta(days=future_days))
        future_time_string = future_time.strftime("%Y-%m-%d")
        events_filter = f"start={actual_time_string}&end={future_time_string}"
        local_calendar_url = f"{self.url}/calendars/{calendar_id}?{events_filter}"    
        headers = {
            'Authorization': f"Bearer {self.token}",
            'Content-Type': 'application/json'
        }
        # Realizar la petición HTTP GET
        response = requests.get(local_calendar_url, headers=headers)
        list_events_data = response.json()
        list_events = []
        for event in list_events_data:
            list_events.append(Calendar.create_event_from_json(calendar_id,event))
        return list_events
    

    def get_history(self, entity_id):
        # Obtener el historial de la entidad
        params = {'filter_entity_id': entity_id}
        headers = {
            'Authorization': f"Bearer {self.token}",
            'Content-Type': 'application/json'
        }
        response = requests.get(self.url + '/history/period', params=params, headers=headers)
        history = response.json()
        return history
    
    def update_events_by_calendar(self):
        for calendar in self.important_calendars:
            calendar_id = calendar.calendar_id
            calendar.set_events(self.requests_calendar_events(calendar_id))

    def update_sensors(self,data):
        valid_sensors_by_id = {sensor['entity_id']: sensor for sensor in data if Sensor.is_valid(sensor)}
        for sensor_aux in self.sensors:
            if(sensor_aux.entity_id in valid_sensors_by_id):
                sensor_data = valid_sensors_by_id[sensor_aux.entity_id]
                sensor_aux.set_value(sensor_data['state'],sensor_data['attributes'].get('unit_of_measurement'))

    def update_binary_sensors(self,data):
        valid_sensors_by_id = {sensor['entity_id']: sensor for sensor in data if BinarySensor.is_valid(sensor)}
        for binary_sensor in self.binary_sensors:
            if(binary_sensor.entity_id in valid_sensors_by_id):
                sensor_data = valid_sensors_by_id[binary_sensor.entity_id]
                binary_sensor.set_value(sensor_data['state'],sensor_data['attributes'].get('unit_of_measurement'))

    def update_general_devices(self,data):
        general_devices_by_id = {device.entity_id: device for device in self.general_devices}
        for sensor_data in data:
            device_found = general_devices_by_id.get(sensor_data['entity_id'])
            if(device_found):
                device_found.set_state(sensor_data['state'])

    def update_person_state(self,data):
        person_state_by_id = {person.entity_id: person for person in self.person_status}
        for person_data in data:
            person_found = person_state_by_id.get(person_data['entity_id'])
            if(person_found): 
                last_not_home_change = self.get_last_not_home_change(person_data['entity_id'])
                person_found.set_state(person_data['state'],person_data['last_changed'],person_data['last_updated'],last_not_home_change)

    def get_last_not_home_change(self,entity_id):
        history = self.get_history(entity_id)
        not_home_states = [state for state in history[0] if state["state"] == "not_home"]
        if(len(not_home_states)>0):
            latest_not_home_state = max(not_home_states, key=lambda x: x["last_changed"])
            return latest_not_home_state["last_changed"]
        else:
            actual_date = datetime.now(timezone.utc)
            day_before = actual_date - timedelta(hours=24)
            day_before_format = day_before.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
            return day_before_format
        

    @classmethod
    def from_json(cls, json_config):
        config = json_config["homeAssistant"]
        url = config['url']
        ha_token = config['haToken']
        people = config['people']
        calendars = config['calendars']
        binary_sensors = config['binarySensors']
        general_devices = config['generalDevices']
        list_sensors = config['sensors']
        return HomeAssistantServices(url, ha_token, people, calendars, list_sensors, binary_sensors, general_devices)