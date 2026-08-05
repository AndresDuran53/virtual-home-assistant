#!/usr/bin/env python3

import sys
import os
from datetime import datetime

# Allow imports from the virtualHomeAssistant package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "virtualHomeAssistant"))

from utils.configuration_reader import ConfigurationReader
from services.homeassistant_services import HomeAssistantServices
from controllers.people_manager import PeopleManager


def print_separator(char: str = "-", width: int = 60) -> None:
    print(char * width)


def main() -> None:
    config_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "configuration.json"
    )
    config_path = os.path.abspath(config_path)

    print(f"Loading config from: {config_path}")
    config = ConfigurationReader.read_config_file(config_path)

    print("Connecting to Home Assistant and fetching data…")
    ha = HomeAssistantServices.from_json(config)

    people = ha.get_people_information()
    manager = PeopleManager(people)

    print_separator("=")
    print("PEOPLE STATUS REPORT")
    print(f"System time     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_separator("=")

    for person in people:
        print(f"\nName            : {person.name}")
        print(f"Entity ID       : {person.entity_id}")
        print(f"State           : {person.state}")
        print(f"Is home         : {person.is_home()}")
        print(f"Just got home   : {person.just_get_home(minutes_to_evaluate=10)}")
        print(f"Last changed    : {person.last_changed}")
        print(f"Last updated    : {person.last_updated}")
        print(f"Last left home  : {person.last_not_home_change}")

        if person.is_home():
            print(f"Time outside    : {person.calculate_total_time_outside()}")

        print_separator()

    print("\nSUMMARY")
    print_separator()
    print(manager.arriving_to_text())
    print(manager.already_home_to_text())
    print(manager.not_home_to_text())
    print_separator("=")


if __name__ == "__main__":
    main()
