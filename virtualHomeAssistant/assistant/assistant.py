import time
from utils.custom_logging import CustomLogging
from assistant.listener import Listener
from assistant.voice import Voice
from assistant.conversation_processor import ConversationProcessor
from controllers.message_processor import MessageProcessor

class Assistant:
    def __init__(self, listener: Listener, 
                 voice: Voice, 
                 conversation_processor: ConversationProcessor,
                 message_processor: MessageProcessor,
                 logger: CustomLogging, 
                 data_config: dict):
        self.logger = logger
        self.data_config = data_config
        self.listener = listener
        self.voice = voice
        self.conversation_processor = conversation_processor
        self.message_processor = message_processor

    def listen(self):
        text_revieced = self.listener.get_next_message()
        text_to_send = self.message_processor.evaluate_default_commands(text_revieced)
        if(text_to_send):
            self.voice.reproduce_sound("assistantRecognition")
            self.logger.info(f"[SST detected] Sending text to conversation processor: {text_to_send}")
            self.start_conversation(text_to_send)

    def start_conversation(self,user_input: str):
        gpt3_response = self.conversation_processor.send_message(user_input)
        if(gpt3_response):
            self.logger.info("Sending response to speakers via mqtt.")
            self.voice.speak(gpt3_response,"es")
            self.logger.info("Response sended.")
        
    def loop(self):
        while True:
            self.listen()
            time.sleep(0.2)

if __name__ == '__main__':
    assistant = Assistant()
    assistant.loop()