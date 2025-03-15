from datetime import datetime
from services.homeassistant_services import HomeAssistantServices
from dto.homeassistant.person import Person
from dto.homeassistant.calendar import Calendar
from controllers.people_manager import PeopleManager


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

    def get_sensors_information(self) -> list:
        return self.sensors_information
    
    def get_datetime_registers(self) -> list:
        return self.datetime_registers_information
    
    def get_general_devices_information(self) -> list:
        return self.general_devices_information
    
    def get_important_devices(self) -> list:
        final_list = []
        final_list += [sensor for sensor in self.sensors_information if not (sensor.needs_to_be_ignore())]
        final_list += [general_device for general_device in self.general_devices_information if not (general_device.needs_to_be_ignore())]
        final_list += [datetime_register for datetime_register in self.datetime_registers_information if not (datetime_register.needs_to_be_ignore())]
        return final_list
    
    def get_people_at_home(self) -> list[Person]:
        people_at_home = self.people_manager.get_people_at_home()
        return people_at_home
    
    def get_people_names_at_home(self) -> list[str]:
        people_at_home = self.get_people_at_home()
        people_names_at_home = [person.name for person in people_at_home]
        return people_names_at_home
    
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

    def get_important_information(self, owner_arrived: bool = False) -> str:
        people_names = []

        if(owner_arrived):
            people_names = self.get_people_names_arriving_home()

        important_devices = self.get_important_devices()
        calendar_events = self.get_calendar_events(people_names)
        all_devices_status = important_devices + calendar_events
        information_text = self.text_from_list(all_devices_status)
        return information_text
    
    def get_maid_information(self) -> str:
        maid_messages = self.text_from_list(self.homeAssistantServices.get_input_texts())
        return maid_messages

    def text_from_list(self, status_list: list) -> str:
        now = datetime.now()
        actual_time_string = now.strftime("Current system time: %A %b %d, %Y at %I:%M%p")
        text = f"\n- {actual_time_string}"
        for element in status_list:
            if(element.to_text() != ""):
                text+=f"\n"
                text += f"- {element.to_text()}"
        return text
    