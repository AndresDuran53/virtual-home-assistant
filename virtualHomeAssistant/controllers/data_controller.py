from services.homeassistant_services import HomeAssistantServices
from dto.homeassistant.person import Person
from dto.homeassistant.calendar import Calendar
from dto.homeassistant.binary_sensor import BinarySensor
from dto.homeassistant.people_manager import PeopleManager


class DataController:
    def __init__(self,data_config):
        self.homeAssistantServices = HomeAssistantServices.from_json(data_config)
        self.update_information()

    def update_information(self):
        self.homeAssistantServices.update_data()
        self.people_information = self.homeAssistantServices.get_people_information()
        self.calendar_events = self.homeAssistantServices.get_calendars_events()
        self.sensors_information = self.homeAssistantServices.get_sensors()
        self.general_devices_information = self.homeAssistantServices.get_general_devices()
        self.datetime_registers_information = self.homeAssistantServices.get_datetime_registers()

    def get_people_information(self) -> list[Person]:
        people_information = self.homeAssistantServices.get_people_information()
        return people_information

    def get_calendar_events(self,calendar_owners:list[str] = []) -> list[Calendar]:
        calendar_events = self.homeAssistantServices.get_calendars_events(calendar_owners)
        return calendar_events

    def get_sensors_information(self) -> list:
        return self.sensors_information
    
    def get_general_devices_information(self) -> list:
        return self.general_devices_information
    
    def get_people_arriving_home(self) -> list:
        peopleManager = PeopleManager(self.people_information)
        people_arriving_home = peopleManager.get_people_just_get_home()
        return people_arriving_home
    
    def get_important_devices(self) -> list:
        final_list = []
        final_list += self.get_sensors_information()
        final_list += [general_device for general_device in self.general_devices_information if not (general_device.needs_to_be_ignore())]
        final_list += [datetime_register for datetime_register in self.datetime_registers_information if not (datetime_register.needs_to_be_ignore())]
        return final_list

