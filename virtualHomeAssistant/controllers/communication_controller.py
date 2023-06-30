from utils.custom_logging import CustomLogging
from services.mqtt_service import MqttConfig, MqttService

class CommunicationController:
    def __init__(self, data_config):
        self.logger = CustomLogging("logs/assistant.log")
        mqtt_config = MqttConfig.from_json(data_config)
        self.mqtt_service = MqttService(mqtt_config, self.handle_command)
        self.pending_commands = []

    def handle_command(self, client, userdata, message):
        topicRecieved = message.topic
        messageRecieved = str(message.payload.decode("utf-8"))
        self.logger.info(f"[Topic]:{topicRecieved} | [Message Recieved]:{messageRecieved}")
        if(messageRecieved == "execute"):
            command = self.mqtt_service.get_command_from_topic(topicRecieved)
            if(command): self.pending_commands.append(command)

    def extract_pending_command(self) -> str:
        if(len(self.pending_commands)>0):
            return self.pending_commands.pop(0)
        return None
    
    def requests_to_reproduce_message(self, message, language="en"):
        if(language=="es"):
            topicPub = "speaker-message/all/tts-es"
        else:
            topicPub = "speaker-message/all/tts"
        self.mqtt_service.send_message(topicPub,message)
