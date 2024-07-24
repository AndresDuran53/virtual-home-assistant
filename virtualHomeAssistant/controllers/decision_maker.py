from utils.custom_logging import CustomLogging
from controllers.data_controller import DataController
from controllers.chat_controller import WelcomeChat,WelcomeGuestChat,GoodMorningChat,FeedCatsReminder
from controllers.user_communication_selector import UserCommunicationSelector
from dto.homeassistant.person import Person

logger = CustomLogging("logs/assistant.log")

class DecisionMaker:

    def __init__(self, data_config: dict):
        self.data_config = data_config
        self.data_controller = DataController(self.data_config)

    def evaluate_default_commands(self, text_received: str) -> str | None:
        if not text_received:
            return None
        elif text_received == "Good Morning":
            return self.create_good_morning_message()
        elif text_received == "Welcome Car":
            return self.create_welcome_chat()
        elif text_received == "Welcome Person":
            return self.create_welcome_chat()
        elif text_received == "Feed Cats Reminder":
            return self.create_cats_reminder()
        else:
            return text_received

    def get_device_information(self, people_names: list[str] = []) -> list:
        important_devices = self.data_controller.get_important_devices()
        calendar_events = self.data_controller.get_calendar_events(people_names)
        return important_devices + calendar_events

    def create_good_morning_message(self) -> str:
        logger.info(f"Creating good morning message.")
        device_information = self.get_device_information()
        logger.info(f"[Home Information]: {[device.to_text() for device in device_information]}")
        user_input = GoodMorningChat.format_good_morning_text(device_information)
        return user_input

    def create_welcome_chat(self) -> str:
        logger.info(f"Creating welcoming message.")
        self.data_controller.update_information()
        people_information = self.data_controller.get_people_information()
        people_arriving_home = UserCommunicationSelector.get_people_arriving_home(people_information)
        if len(people_arriving_home) > 0:
            return self.handle_people_arriving_home(people_arriving_home)
        else:
            logger.info(f"Stopping welcoming, no person arrived.")
            return self.handle_no_people_arrived(people_information)

    def create_cats_reminder(self) -> str:
        user_input = FeedCatsReminder.message()
        return user_input

    def handle_people_arriving_home(self, people_arriving_home: list[Person]) -> str:
        logger.info(f"[People Arriving]: {[person.get_information() for person in people_arriving_home]}")
        people_arriving_names = [person.name for person in people_arriving_home]
        device_information = self.get_device_information(people_arriving_names)
        logger.info(f"[Home Information]: {[device.to_text() for device in device_information]}")
        user_input = WelcomeChat.format_welcome_text(people_arriving_home, device_information)
        return user_input
        
    def handle_no_people_arrived(self, people_information) -> str:
        people_at_home = UserCommunicationSelector.get_people_at_home(people_information)
        logger.info(f"[People At Home]: {[person.get_information() for person in people_at_home]}")
        user_input = WelcomeGuestChat.format_welcome_text(people_at_home)
        return user_input
