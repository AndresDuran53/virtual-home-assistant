from utils.custom_logging import CustomLogging
from controllers.data_controller import DataController
from controllers.chat_controller import WelcomeChat, WelcomeGuestChat, GoodMorningChat, FeedCatsReminder, MaidAnnouncements

logger = CustomLogging("logs/assistant.log")

class DecisionMaker:

    def __init__(self, data_config: dict):
        self.data_config = data_config
        self.data_controller = DataController(self.data_config)

    def evaluate_default_commands(self, text_received: str) -> str | None:
        self.data_controller.update_information()
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
        elif text_received == "Announcements to Maid":
            return self.create_message_maid()
        else:
            return text_received

    def create_good_morning_message(self) -> str:
        logger.info(f"Creating good morning message.")
        internal_information_text = self.data_controller.get_internal_information()
        important_information_text = self.data_controller.get_important_information()
        logger.info(f"[Home Information]: {important_information_text}")
        user_input = GoodMorningChat.format_good_morning_text(internal_information_text, important_information_text)
        return user_input

    def create_welcome_chat(self) -> str:
        logger.info(f"Creating welcoming message.")
        is_people_arriving_home = self.data_controller.is_people_arriving_home()
        if is_people_arriving_home:
            logger.info(f"Welcoming to owner arriving.")
            return self.handle_owner_arriving_home()
        else:
            logger.info(f"Welcoming guest, no owner arrived.")
            return self.handle_guest_arrived()
        
    def create_message_maid(self) -> str:
        logger.info(f"Creating message to maid.")
        maid_information = self.data_controller.get_maid_information()
        logger.info(f"[Maid Information]: {maid_information}")
        user_input = MaidAnnouncements.format_information(maid_information)
        return user_input

    def handle_owner_arriving_home(self) -> str:
        people_arriving_names = self.data_controller.get_people_names_arriving_home()
        logger.info(f"[People Arriving]: {[person_name for person_name in people_arriving_names]}")
        internal_information_text = self.data_controller.get_internal_information()
        logger.info(f"[Internal Information]: {internal_information_text}")
        important_information_text = self.data_controller.get_important_information(True)
        logger.info(f"[Important Information]: {important_information_text}")
        user_input = WelcomeChat.format_welcome_text(people_arriving_names, internal_information_text, important_information_text)
        return user_input
        
    def handle_guest_arrived(self) -> str:
        people_names_at_home = self.data_controller.get_people_names_at_home()
        logger.info(f"[People At Home]: {[person_name for person_name in people_names_at_home]}")
        user_input = WelcomeGuestChat.format_welcome_text(people_names_at_home)
        return user_input

    def create_cats_reminder(self) -> str:
        user_input = FeedCatsReminder.message()
        return user_input