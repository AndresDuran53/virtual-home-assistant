import sys
import os

# adding the parent directory to the sys.path.
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from utils.configuration_reader import ConfigurationReader
from controllers.data_controller import DataController
from dto.homeassistant.person import Person
from dto.homeassistant.calendar import Calendar
from dto.homeassistant.sensor import Sensor

def main():
    data_config = ConfigurationReader.read_config_file()
    data_controller = DataController(data_config)
    test_people_information(data_controller)
    #test_calendars_events(data_controller)
    #test_sensors_information(data_controller)
    #test_general_devices_information(data_controller)
    #test_people_arriving_home(data_controller)
    #test_important_devices(data_controller)

def test_people_information(data_controller:DataController):
    people_information: list[Person] = data_controller.get_people_information()
    for people in people_information:
        print(people.get_information())

def test_calendars_events(data_controller:DataController):
    calendars_events: list[Calendar] = data_controller.get_calendar_events()
    for calendar in calendars_events:
        print(calendar.to_text())

def test_sensors_information(data_controller:DataController):
    sensor_information: list[Sensor] = data_controller.get_sensors_information()
    for sensor in sensor_information:
        print(sensor.to_text())

def test_general_devices_information(data_controller:DataController):
    general_devices_information = data_controller.get_general_devices_information()
    for general_devices in general_devices_information:
        print(general_devices.to_text())

def test_people_arriving_home(data_controller:DataController):
    people_arriving_home: list[Person] = data_controller.get_people_arriving_home()
    for person in people_arriving_home:
        print(person.get_information())

def test_important_devices(data_controller:DataController):
    important_devices = data_controller.get_important_devices()
    for device in important_devices:
        print(device.to_text())
    

if __name__ == "__main__":
    main()
