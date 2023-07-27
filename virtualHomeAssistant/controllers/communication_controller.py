from utils.custom_logging import CustomLogging
from services.mqtt_service import MqttConfig, MqttService

class CommunicationController:
    def __init__(self, data_config):
        self.logger = CustomLogging("logs/assistant.log")
        mqtt_config = MqttConfig.from_json(data_config)
        self.mqtt_service = MqttService(mqtt_config, None)
        self.pending_commands = []
    
    def requests_to_reproduce_message(self, message, language="en"):
        if(language=="es"):
            topicPub = "speaker-message/all/tts-es"
        else:
            topicPub = "speaker-message/all/tts"
        self.mqtt_service.send_message(topicPub,message)

    def requests_to_reproduce_sound(self,sound_name):
        topicPub = "speaker-message/all/reproduce"
        self.mqtt_service.send_message(topicPub,sound_name)
