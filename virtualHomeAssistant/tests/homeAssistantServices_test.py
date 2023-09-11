import sys
import os

# adding the parent directory to the sys.path.
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from utils.configuration_reader import ConfigurationReader
from services.homeassistant_services import HomeAssistantServices
from dto.homeassistant.person import Person
from dto.homeassistant.calendar import Calendar

def main():
    data_config = ConfigurationReader.read_config_file()
    homeAssistantServices = HomeAssistantServices.from_json(data_config)
    test_general_data(homeAssistantServices)
    test_people_information(homeAssistantServices)
    test_calendars_events(homeAssistantServices)

def test_general_data(homeAssistantServices:HomeAssistantServices):
    general_data = homeAssistantServices.requests_general_data()
    print(general_data)

def test_people_information(homeAssistantServices:HomeAssistantServices):
    people_information: list[Person] = homeAssistantServices.get_people_information()
    for people in people_information:
        print(people.get_information())

def test_calendars_events(homeAssistantServices:HomeAssistantServices):
    calendars_events: list[Calendar] = homeAssistantServices.get_calendars_events()
    for calendar in calendars_events:
        print(calendar.to_text())
    

if __name__ == "__main__":
    main()

