import os
import sys

here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '..'))

from utils.configuration_reader import ConfigurationReader
from controllers.data_controller import DataController

def main():
    print("Starting test")
    data_config = ConfigurationReader.read_config_file()
    data_controller = DataController(data_config)
    important_devices = data_controller.get_important_devices()
    for device in important_devices:
        print(device.to_text())
    calendar_events = data_controller.get_calendar_events()
    for calendar in calendar_events:
        print(calendar.to_text())

if __name__ == "__main__":
    main()