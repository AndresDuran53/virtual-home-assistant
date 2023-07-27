import time
import threading
from utils.custom_logging import CustomLogging
from assistant.listener import Listener
from controllers.communication_controller import CommunicationController
from controllers.data_controller import DataController
from utils.csv_storage import CSVStorage
from services.gpt_service import OpenAIGPT3
from controllers.chat_controller import WelcomeChat,WelcomeGuestChat,GoodMorningChat,FeedCatsReminder
from controllers.user_communication_selector import UserCommunicationSelector
from whisper_transcribe.speech_handler import SpeechHandler

class Assistant:
    def __init__(self, listener: Listener, logger: CustomLogging, data_config: dict):
        self.logger = logger
        self.data_config = data_config
        self.logger.info(f"Connecting to Listener...")
        self.listener = listener
        self.logger.info(f"Connecting to Communication Manager...")
        self.communication_controller = CommunicationController(self.data_config)
        self.logger.info(f"Creating data manager...")
        self.data_controller = DataController(self.data_config)
        self.logger.info(f"Creating OpenAi GPT3 service...")
        self.chat_service = OpenAIGPT3.from_json(self.data_config)
        self.logger.info(f"Creating token manager...")
        self.token_manager = CSVStorage(self.chat_service.used_chars_filename)
        self.start_audio_translation()

    def start_audio_translation(self):
        self.speechHandler = SpeechHandler()
        speech_thread = threading.Thread(target=self.speechHandler.execute)
        speech_thread.start()

    def check_pending_commands(self):
        command_aux = self.listener.get_next_message()
        if(command_aux == "Good Morning"):
            self.create_good_moning_message()
        elif(command_aux == "Welcome Car"):
            self.create_welcome_chat(True)
        elif(command_aux == "Welcome Person"):
            self.create_welcome_chat()
        elif(command_aux == "Feed Cats Reminder"):
            self.create_cats_reminder()

    def get_device_information(self):
        important_devices = self.data_controller.get_important_devices()
        calendar_events = self.data_controller.get_calendar_events()
        return important_devices + calendar_events
    
    def send_conversation_to_gpt3(self,user_input):
        gpt3_response = self.send_message_to_gpt3(user_input)
        if(gpt3_response):
            self.logger.info("Sending response to speakers via mqtt.")
            self.communication_controller.requests_to_reproduce_message(gpt3_response,"es")
            self.logger.info("Response sended.")
    
    def create_good_moning_message(self):
        self.logger.info(f"Creating good morning message.")
        device_information = self.get_device_information()
        self.logger.info(f"[Home Information]: {[device.to_text() for device in device_information]}")
        user_input = GoodMorningChat.format_good_morning_text(device_information)
        self.send_conversation_to_gpt3(user_input)

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
        self.send_conversation_to_gpt3(user_input)
        
    def handle_no_people_arrived(self, people_information):
        people_at_home = UserCommunicationSelector.get_people_at_home(people_information)
        self.logger.info(f"[People At Home]: {[person.get_information() for person in people_at_home]}")
        user_input = WelcomeGuestChat.format_welcome_text(people_at_home)
        self.send_conversation_to_gpt3(user_input)

    def create_cats_reminder(self):
        user_input = FeedCatsReminder.message()
        self.send_conversation_to_gpt3(user_input)

    def send_message_to_gpt3(self,user_input):
        if(user_input == None and user_input == ""): return
        max_per_day = self.token_manager.get_value_for_date()
        self.logger.info(f"[Tokens used today]: {max_per_day}")
        if(self.chat_service.can_do_question(user_input,max_per_day)):
            self.logger.info("Sending request to openai api.")
            text_result,total_tokens = self.chat_service.welcome_home_chat(user_input)
            self.logger.info(f"[GPT3 Response]: {text_result}")
            self.token_manager.increase_value_for_today_by(total_tokens)
            self.logger.info(f"[Total tokens used]: {total_tokens}")
            return text_result
        else:
            self.logger.warning("Too many tokens to request.")
            return None
        
    def loop(self):
        while True:
            self.check_pending_commands()
            if(len(self.speechHandler.last_mention)>0):
                self.communication_controller.requests_to_reproduce_sound("assistantRecognition")
                texto_a_enviar = self.speechHandler.last_mention.pop(-1)
                print(f"Texto a enviar: {texto_a_enviar}")
                self.send_conversation_to_gpt3(texto_a_enviar)
            time.sleep(0.2)

if __name__ == '__main__':
    assistant = Assistant()
    assistant.loop()