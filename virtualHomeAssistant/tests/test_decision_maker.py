import sys
import os

# adding the parent directory to the sys.path.
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from utils.configuration_reader import ConfigurationReader
from controllers.decision_engine import DecisionMaker

def main():
    data_config = ConfigurationReader.read_config_file()
    decision_maker = DecisionMaker(data_config)
    test_create_good_morning_message(decision_maker)
    #test_create_welcome_chat_car(decision_maker)
    #test_create_welcome_chat_owner(decision_maker)
    #test_create_welcome_chat_person(decision_maker)
    #test_create_cats_reminder(decision_maker)


def test_create_good_morning_message(decision_maker:DecisionMaker):
    result1 = decision_maker.evaluate_default_commands("Good Morning")
    print(result1)
    print("\n--------------------------------------------\n\n")

def test_create_welcome_chat_car(decision_maker:DecisionMaker):
    result2 = decision_maker.evaluate_default_commands("Welcome Car")
    print(result2)
    print("\n--------------------------------------------\n\n")

def test_create_welcome_chat_owner(decision_maker:DecisionMaker):
    result3 = decision_maker.evaluate_default_commands("Welcome Owner")
    print(result3)
    print("\n--------------------------------------------\n\n")

def test_create_welcome_chat_person(decision_maker:DecisionMaker):
    result3 = decision_maker.evaluate_default_commands("Welcome Person")
    print(result3)
    print("\n--------------------------------------------\n\n")

def test_create_cats_reminder(decision_maker:DecisionMaker):
    result4 = decision_maker.evaluate_default_commands("Feed Cats Reminder")
    print(result4)
    print("\n--------------------------------------------\n\n")


if __name__ == "__main__":
    main()
