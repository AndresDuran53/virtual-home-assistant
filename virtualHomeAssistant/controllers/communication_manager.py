from utils.custom_logging import CustomLogging
from services.mqtt_controller import MqttConfig, MqttController

class CommunicationManager:
    def __init__(self, data_config):
        self.logger = CustomLogging("logs/assistant.log")
        mqtt_config = MqttConfig.from_json(data_config)
        self.mqtt_controller = MqttController(mqtt_config, self.handle_command)
        self.pending_commands = []

    def handle_command(self, client, userdata, message):
        topicRecieved = message.topic
        messageRecieved = str(message.payload.decode("utf-8"))
        self.logger.info(f"[Topic]:{topicRecieved} | [Message Recieved]:{messageRecieved}")
        if(messageRecieved == "execute"):
            command = self.mqtt_controller.get_command_from_topic(topicRecieved)
            if(command): self.pending_commands.append(command)

    def extract_pending_command(self) -> str:
        if(len(self.pending_commands)>0):
            return self.pending_commands.pop(0)
        return None
    
    def requests_to_reproduce_message(self, message, language="en"):
        if(language=="es"):
            topicPub = "speaker-message/nag241/tts-es"
        else:
            topicPub = "speaker-message/nag241/tts"
        self.mqtt_controller.send_message(topicPub,message)
