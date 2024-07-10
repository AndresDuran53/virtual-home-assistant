import os
import sys

here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '..'))

from utils.configuration_reader import ConfigurationReader
from controllers.data_controller import DataController
from dto.homeassistant.entity import Entity
from dto.homeassistant.sensor import Sensor

def main():
    print("Starting test")
    data_config = ConfigurationReader.read_config_file()
    data_controller = DataController(data_config)
    important_devices = data_controller.get_important_devices()
    for device in important_devices:
        print(device.to_text())
        check_entity(device)
    calendar_events = data_controller.get_calendar_events()
    for calendar in calendar_events:
        print(calendar.to_text())

def check_entity(device):
    text: str = device.to_text()
    if text.startswith("House Temperature"):
        new_entity: Sensor = device
        print(f"Entity Class: {new_entity.entity_class}")

if __name__ == "__main__":
    main()