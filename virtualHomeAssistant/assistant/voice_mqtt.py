from assistant.voice import Voice
from utils.custom_logging import CustomLogging
from services.mqtt_service import MqttConfig, MqttService

logger = CustomLogging("logs/assistant.log")

class VoiceMqtt(Voice):
    mqtt_service: MqttService


    def __init__(self, data_config: dict):
        mqtt_config = MqttConfig.from_json(data_config)
        self.mqtt_service = MqttService(mqtt_config, None)
        print(f"VoiceMqtt: {self.mqtt_service}")
    
    def speak(self, message: str, language="en"):
        if(language=="es"):
            topicPub = "speaker-message/all/tts-es"
        else:
            topicPub = "speaker-message/all/tts"
        self.mqtt_service.send_message(topicPub,message)

    def reproduce_sound(self,sound_name):
        topicPub = "speaker-message/all/reproduce"
        self.mqtt_service.send_message(topicPub,sound_name)
