import time
from utils.custom_logging import CustomLogging
from assistant.listener import Listener
from assistant.voice import Voice
from assistant.conversation_processor import ConversationProcessor
from controllers.data_controller import DataController
from controllers.chat_controller import WelcomeChat,WelcomeGuestChat,GoodMorningChat,FeedCatsReminder
from controllers.user_communication_selector import UserCommunicationSelector

class Assistant:
    def __init__(self, listener: Listener, 
                 voice: Voice, 
                 conversation_processor: ConversationProcessor,
                 logger: CustomLogging, 
                 data_config: dict):
        self.logger = logger
        self.data_config = data_config
        self.listener = listener
        self.voice = voice
        self.data_controller = DataController(self.data_config)
        self.conversation_processor = conversation_processor

    def listen(self):
        text_revieced = self.listener.get_next_message()
        if(not text_revieced): return
        if(text_revieced == "Good Morning"):
            self.create_good_moning_message()
        elif(text_revieced == "Welcome Car"):
            self.create_welcome_chat(True)
        elif(text_revieced == "Welcome Person"):
            self.create_welcome_chat()
        elif(text_revieced == "Feed Cats Reminder"):
            self.create_cats_reminder()
        else:
            self.voice.reproduce_sound("assistantRecognition")
            self.logger.info(f"[SST detected] Sending text to conversation processor: {text_revieced}")
            self.start_conversation(text_revieced)

    def start_conversation(self,user_input: str):
        gpt3_response = self.conversation_processor.send_message(user_input)
        if(gpt3_response):
            self.logger.info("Sending response to speakers via mqtt.")
            self.voice.speak(gpt3_response,"es")
            self.logger.info("Response sended.")

    def get_device_information(self):
        important_devices = self.data_controller.get_important_devices()
        calendar_events = self.data_controller.get_calendar_events()
        return important_devices + calendar_events
    
    def create_good_moning_message(self):
        self.logger.info(f"Creating good morning message.")
        device_information = self.get_device_information()
        self.logger.info(f"[Home Information]: {[device.to_text() for device in device_information]}")
        user_input = GoodMorningChat.format_good_morning_text(device_information)
        self.start_conversation(user_input)

    def create_welcome_chat(self, notify_no_people = False):
        self.logger.info(f"Creating welcoming message.")
        self.data_controller.update_information()
        people_information = self.data_controller.get_people_information()
        people_arriving_home = UserCommunicationSelector.get_people_arriving_home(people_information)
        if len(people_arriving_home) > 0:
            self.handle_people_arriving_home(people_arriving_home)
        elif notify_no_people:
            self.logger.info(f"Stopping welcoming, no person arrived.")
            self.handle_no_people_arrived(people_information)
        
    def handle_people_arriving_home(self, people_arriving_home):
        self.logger.info(f"[People Arriving]: {[person.get_information() for person in people_arriving_home]}")
        device_information = self.get_device_information()
        self.logger.info(f"[Home Information]: {[device.to_text() for device in device_information]}")
        user_input = WelcomeChat.format_welcome_text(people_arriving_home, device_information)
        self.start_conversation(user_input)
        
    def handle_no_people_arrived(self, people_information):
        people_at_home = UserCommunicationSelector.get_people_at_home(people_information)
        self.logger.info(f"[People At Home]: {[person.get_information() for person in people_at_home]}")
        user_input = WelcomeGuestChat.format_welcome_text(people_at_home)
        self.start_conversation(user_input)

    def create_cats_reminder(self):
        user_input = FeedCatsReminder.message()
        self.start_conversation(user_input)
        
    def loop(self):
        while True:
            self.listen()
            time.sleep(0.2)

if __name__ == '__main__':
    assistant = Assistant()
    assistant.loop()