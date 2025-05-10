from typing import Optional, Sequence
from datetime import datetime
from services.homeassistant_services import HomeAssistantServices
from dto.homeassistant.person import Person
from dto.homeassistant.calendar import Calendar
from controllers.people_manager import PeopleManager
from dto.homeassistant.sensor import Sensor
from dto.homeassistant.datetime_register import DatetimeRegister
from dto.homeassistant.device import Device
from dto.homeassistant.entity import Entity


class DataController:
    def __init__(self, data_config: dict):
        self.homeAssistantServices = HomeAssistantServices.from_json(data_config)
        self.people_manager = PeopleManager()
        self.update_information()

    def update_information(self):
        self.homeAssistantServices.update_data()
        self.people_information = self.homeAssistantServices.get_people_information()
        self.people_manager.set_people_list(self.people_information)
        self.calendar_events = self.homeAssistantServices.get_calendars_events()
        self.sensors_information = self.homeAssistantServices.get_sensors()
        self.general_devices_information = self.homeAssistantServices.get_general_devices()
        self.datetime_registers_information = self.homeAssistantServices.get_datetime_registers()

    def get_people_information(self) -> list[Person]:
        return self.people_information

    def get_calendar_events(self, calendar_owners:list[str] = []) -> list[Calendar]:
        calendar_events = self.homeAssistantServices.get_calendars_events(calendar_owners)
        return calendar_events

    def get_sensors_information(self) -> list[Sensor]:
        return self.sensors_information
    
    def get_general_devices_information(self) -> list[Device]:
        return self.general_devices_information
    
    def get_datetime_registers(self) -> list[DatetimeRegister]:
        return self.datetime_registers_information
    
    def get_all_devices(self , visibility: Optional[str] = None) -> list[Entity]:
        def filter_entities(entities: Sequence[Entity]):
            return [
                entity for entity in entities
                if not entity.needs_to_be_ignore() and (not visibility or entity.get_visibility() == visibility)
            ]

        all_devices = (
            filter_entities(self.get_sensors_information()) +
            filter_entities(self.get_general_devices_information()) +
            filter_entities(self.get_datetime_registers())
        )
            
        return all_devices

    
    def get_people_at_home(self) -> list[Person]:
        people_at_home = self.people_manager.get_people_at_home()
        return people_at_home
    
    def get_people_names_at_home(self) -> list[str]:
        """
        Returns a list of names of people currently at home.
        """
        return [person.name for person in self.get_people_at_home()]
    
    def get_people_arriving_home(self) -> list[Person]:
        people_arriving_home = self.people_manager.get_people_just_get_home()
        return people_arriving_home
    
    def get_people_names_arriving_home(self) -> list[str]:
        people_arriving_home = self.get_people_arriving_home()
        people_names_arriving_home = [person.name for person in people_arriving_home]
        return people_names_arriving_home
    
    def is_people_arriving_home(self) -> bool:
        people_names_arriving_home = self.get_people_names_arriving_home()
        result = len(people_names_arriving_home) > 0
        return result
    
    def get_internal_information(self) -> str:
        now = datetime.now()
        actual_time_string = now.strftime("Current system time: %A %b %d, %Y at %I:%M%p")
        fina_text = f"\n- {actual_time_string}"

        internal_information = self.get_all_devices(visibility='internal')
        information_text = self.text_from_list(internal_information)

        fina_text += information_text
        return fina_text

    def get_important_information(self, owner_arrived: bool = False) -> str:
        people_names = []

        if(owner_arrived):
            people_names = self.get_people_names_arriving_home()

        important_devices = self.get_all_devices(visibility='important')
        calendar_events = self.get_calendar_events(people_names)
        all_devices_status = important_devices + calendar_events
        information_text = self.text_from_list(all_devices_status)

        return information_text
    
    def get_maid_information(self) -> str:
        maid_messages = self.text_from_list(self.homeAssistantServices.get_input_texts())
        return maid_messages

    def text_from_list(self, status_list: list) -> str:
        text = ''
        for element in status_list:
            if(element.to_text() != ""):
                text+=f"\n"
                text += f"- {element.to_text()}"
        return text
