from homeassistant_services import HomeAssistantServices
from libs.person import Person

class DataManager:
    def __init__(self,data_config):
        self.homeAssistantServices = HomeAssistantServices.from_json(data_config)
        self.update_information()

    def update_information(self):
        self.homeAssistantServices.update_data()
        self.people_information = self.homeAssistantServices.get_people_information()
        self.calendar_events = self.homeAssistantServices.get_calendars_events()
        self.sensors_information = self.homeAssistantServices.get_sensors()
        self.general_devices_information = self.homeAssistantServices.get_general_devices()

    def get_people_information(self) -> list:
        return self.people_information

    def get_calendar_events(self) -> list:
        return self.calendar_events

    def get_sensors_information(self) -> list:
        return self.sensors_information
    
    def get_general_devices_information(self) -> list:
        return self.general_devices_information
    
    def get_people_arriving_home(self) -> list:
        people_arriving_home = Person.get_people_just_get_home(self.people_information)
        return people_arriving_home
    
    def get_important_devices(self):
        final_list = []
        final_list += self.get_sensors_information()
        final_list += self.get_general_devices_information()
        return final_list

