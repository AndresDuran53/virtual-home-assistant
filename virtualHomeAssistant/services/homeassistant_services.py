import requests
import json
from datetime import datetime,timedelta,timezone
from dto.homeassistant.device import Device
from dto.homeassistant.calendar import Calendar
from dto.homeassistant.event import Event
from dto.homeassistant.sensor import Sensor
from dto.homeassistant.binary_sensor import BinarySensor
from dto.homeassistant.person import Person
from dto.homeassistant.person_location_status import PersonLocationStatus
from dto.homeassistant.datetime_register import DatetimeRegister

class HomeAssistantServices:
    url: str
    token: str
    person_status: list[Person]
    important_calendars: list[Calendar]
    sensors: list[Sensor]
    binary_sensors: list[BinarySensor]
    general_devices: list[Device]
    datetime_registers: list[DatetimeRegister]

    def __init__(self, url, token, people, calendars, list_sensors, binary_sensors, general_devices, list_datetime_register):
        self.url = url
        self.token = token
        self._filling_list_devices(people, calendars, list_sensors, binary_sensors, general_devices, list_datetime_register)
        self.update_data()

    def _filling_list_devices(self, 
                              people: list[dict], 
                              list_calendar: list[dict], 
                              list_sensors: list[dict], 
                              list_binary_sensors: list[dict], 
                              list_general_devices: list[dict],
                              list_datetime_register: list[dict]):
        self.person_status = Person.list_from_dict(people)
        self.sensors = Sensor.list_from_dict(list_sensors)
        self.binary_sensors = BinarySensor.list_from_dict(list_binary_sensors)
        self.general_devices = Device.list_from_dict(list_general_devices)
        self.datetime_registers = DatetimeRegister.list_from_dict(list_datetime_register)
        self.important_calendars = Calendar.list_from_dict(list_calendar)

    def make_request(self, url: str, params = None):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, params=params, headers=headers)
        return response.json()
    
    def requests_general_data(self):
        url = self.url + "/states"
        data = self.make_request(url)
        return data

    def get_history(self, entity_id: str):
        url = self.url + "/history/period"
        params = {'filter_entity_id': entity_id}
        history = self.make_request(url, params)
        return history

    def update_data(self):
        self.last_data=self.requests_general_data()
        self.update_sensors(self.last_data)
        self.update_events_by_calendar()
    
    def get_people_information(self) -> list[Person]:
        return self.person_status
        
    def get_sensors(self) -> list[Sensor]:
        return self.sensors + self.binary_sensors
    
    def get_general_devices(self) -> list[Device]:
        return self.general_devices
    
    def get_datetime_registers(self) -> list[DatetimeRegister]:
        return self.datetime_registers
    
    def get_calendars_events(self, calendar_owners:list[str] = []) -> list[Calendar]:
        if(not calendar_owners):
            return self.important_calendars
        else:
            shared_calendars = [calendar for calendar in self.important_calendars if any(owner in calendar.calendar_owner for owner in calendar_owners)]
        return shared_calendars
    
    def update_sensors(self, data):
        for entity_data in data:
            
            if (Sensor.is_valid(entity_data)):
                for sensor_aux in self.sensors:
                    if(sensor_aux.entity_id == entity_data['entity_id']):
                        sensor_aux.set_state(entity_data['state'],entity_data['attributes'].get('unit_of_measurement'))
            
            elif (BinarySensor.is_valid(entity_data)):
                for sensor_aux in self.binary_sensors:
                    if(sensor_aux.entity_id == entity_data['entity_id']):
                        sensor_aux.set_state(entity_data['state'],entity_data['attributes'].get('unit_of_measurement'))
            
            elif (Person.is_valid(entity_data)):
                for sensor_aux in self.person_status:
                    if(sensor_aux.entity_id == entity_data['entity_id']):
                        last_not_home_change = self.get_last_not_home_change(entity_data.get('entity_id'))
                        if(last_not_home_change):
                            sensor_aux.set_state(entity_data['state'],entity_data['last_changed'],entity_data['last_updated'],last_not_home_change)

            if (DatetimeRegister.is_valid(entity_data)):
                for sensor_aux in self.datetime_registers:
                    if(sensor_aux.entity_id == entity_data['entity_id']):
                        sensor_aux.set_state(entity_data['state'])

            else:
                for sensor_aux in self.general_devices:
                    if(sensor_aux.entity_id == entity_data['entity_id']):
                        sensor_aux.set_state(entity_data['state'])

    def get_last_not_home_change(self, entity_id: str | None):
        if (not entity_id):
            return None
        history = self.get_history(entity_id)
        person_statuses = PersonLocationStatus.create_person_statuses(history)
        personLocationStatusAway = PersonLocationStatus.find_statuses(person_statuses)
        if(personLocationStatusAway and personLocationStatusAway.last_changed):
            return personLocationStatusAway.last_changed
        else:
            actual_date = datetime.now(timezone.utc)
            day_before = actual_date - timedelta(hours=24)
            day_before_format = day_before.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
            return day_before_format
        
    def update_events_by_calendar(self):
        for calendar in self.important_calendars:
            calendar_id = calendar.calendar_id
            calendar.set_events(self.requests_calendar_events(calendar_id))

    def requests_calendar_events(self, calendar_id: str, future_days = 3) -> list[Event]:
        now = datetime.now()
        actual_time_string = now.strftime("%Y-%m-%d")
        future_time = now + timedelta(days=future_days)
        future_time_string = future_time.strftime("%Y-%m-%d")
        events_filter = f"start={actual_time_string}&end={future_time_string}"
        local_calendar_url = f"{self.url}/calendars/{calendar_id}?{events_filter}"
        list_events_data = self.make_request(local_calendar_url)
        list_events = [Calendar.create_event_from_json(calendar_id, event) for event in list_events_data]
        return list_events
    
    @classmethod
    def from_json(cls, json_config: dict):
        config: dict = json_config.get("homeAssistant",{})
        url = config.get('url')
        ha_token = config.get('haToken')
        people = config.get('people')
        calendars = config.get('calendars')
        binary_sensors = config.get('binarySensors')
        general_devices = config.get('generalDevices')
        list_sensors = config.get('sensors')
        list_datetime_register = config.get('datetimeRegister')
        return HomeAssistantServices(url, ha_token, people, calendars, list_sensors, binary_sensors, general_devices, list_datetime_register)