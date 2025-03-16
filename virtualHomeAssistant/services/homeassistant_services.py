import requests
from typing import Type, Sequence, Optional
from datetime import datetime, timedelta, timezone
from dto.homeassistant.entity import Entity
from dto.homeassistant.device import Device
from dto.homeassistant.calendar import Calendar
from dto.homeassistant.event import Event
from dto.homeassistant.sensor import Sensor
from dto.homeassistant.binary_sensor import BinarySensor
from dto.homeassistant.person import Person
from dto.homeassistant.input_text import InputText
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
    input_texts: list[InputText]

    def __init__(
        self,
        url: str,
        token: str,
        people: list[dict],
        calendars: list[dict],
        sensors: list[dict],
        binary_sensors: list[dict],
        devices: list[dict],
        datetime_registers: list[dict],
        input_texts: list[dict],
    ):
        self.url = url
        self.token = token
        self.person_status = Person.list_from_dict(people)
        self.sensors = Sensor.list_from_dict(sensors)
        self.binary_sensors = BinarySensor.list_from_dict(binary_sensors)
        self.general_devices = Device.list_from_dict(devices)
        self.datetime_registers = DatetimeRegister.list_from_dict(datetime_registers)
        self.important_calendars = Calendar.list_from_dict(calendars)
        self.input_texts = InputText.list_from_dict(input_texts)
        self.update_data()

    def _make_request(self, endpoint: str, params=None):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.get(f"{self.url}{endpoint}", params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error on the request: {e}")
            return None

    def requests_general_data(self):
        return self._make_request("/states")

    def get_history(self, entity_id: str):
        return self._make_request("/history/period", {"filter_entity_id": entity_id})

    def update_data(self):
        data = self.requests_general_data()
        if data:
            self.update_sensors(data)
            self.update_events_by_calendar()

    def get_people_information(self) -> list[Person]:
        return self.person_status

    def get_sensors(self) -> list[Sensor]:
        return self.sensors + self.binary_sensors

    def get_general_devices(self) -> list[Device]:
        return self.general_devices

    def get_datetime_registers(self) -> list[DatetimeRegister]:
        return self.datetime_registers

    def get_input_texts(self) -> list[InputText]:
        return self.input_texts

    def get_calendars_events(self, calendar_owners: list[str] = []) -> list[Calendar]:
        if not calendar_owners:
            return self.important_calendars
        else:
            shared_calendars = [
                calendar
                for calendar in self.important_calendars
                if any(owner in calendar.calendar_owner for owner in calendar_owners)
            ]
        return shared_calendars
    
    def update_sensors(self, data):
        entity_types: dict[Type[Entity], Sequence[Entity]] = {
            Person: self.person_status,
            Sensor: self.sensors,
            BinarySensor: self.binary_sensors,
            DatetimeRegister: self.datetime_registers,
            InputText: self.input_texts,
        }

        for entity_data in data:
            entity_id = entity_data.get("entity_id")
            state = entity_data.get("state")
            attributes = entity_data.get("attributes", {})
            unit = attributes.get("unit_of_measurement", "")
            last_changed = entity_data.get("last_changed")
            last_updated = entity_data.get("last_updated")

            for entity_class, sensors in entity_types.items():
                if entity_class.is_valid(entity_data):
                    for sensor in sensors:
                        if sensor.entity_id == entity_id:
                            if isinstance(sensor, Person):
                                last_not_home_change = self.get_last_not_home_change(entity_id)
                                if last_not_home_change:
                                    sensor.set_state(state, last_changed, last_updated, last_not_home_change)
                            else:
                                sensor.set_state(state=state, unit=unit)
                    break
            else:
                for sensor in self.general_devices:
                    if sensor.entity_id == entity_id:
                        sensor.set_state(state=state, unit=unit)

    def get_last_not_home_change(self, entity_id: str | None):
        if not entity_id:
            return None
        history = self.get_history(entity_id)
        person_statuses = PersonLocationStatus.create_person_statuses(history)
        personLocationStatusAway = PersonLocationStatus.find_statuses(person_statuses)
        if personLocationStatusAway and personLocationStatusAway.last_changed:
            return personLocationStatusAway.last_changed
        else:
            actual_date = datetime.now(timezone.utc)
            day_before = actual_date - timedelta(hours=24)
            day_before_format = day_before.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")
            return day_before_format

    def update_events_by_calendar(self):
        for calendar in self.important_calendars:
            calendar_id = calendar.calendar_id
            calendar.set_events(self.requests_calendar_events(calendar_id))

    def requests_calendar_events(self, calendar_id: str, future_days=3) -> list[Event]:
        now = datetime.now()
        actual_time_string = now.strftime("%Y-%m-%d")
        future_time = now + timedelta(days=future_days)
        future_time_string = future_time.strftime("%Y-%m-%d")
        events_filter = f"start={actual_time_string}&end={future_time_string}"
        local_calendar_endpoint = f"/calendars/{calendar_id}?{events_filter}"
        list_events_data = self._make_request(local_calendar_endpoint)
        list_events = [
            Calendar.create_event_from_json(calendar_id, event)
            for event in list_events_data
        ]
        return list_events

    @classmethod
    def from_json(cls, json_config: dict):
        config: dict = json_config.get("homeAssistant", {})
        url = config.get("url")
        ha_token = config.get("haToken")
        people = config.get("people")
        calendars = config.get("calendars")
        binary_sensors = config.get("binarySensors")
        general_devices = config.get("generalDevices")
        list_sensors = config.get("sensors")
        list_datetime_register = config.get("datetimeRegister")
        list_input_texts = config.get("input_text")
        return HomeAssistantServices(
            url,
            ha_token,
            people,
            calendars,
            list_sensors,
            binary_sensors,
            general_devices,
            list_datetime_register,
            list_input_texts,
        )
