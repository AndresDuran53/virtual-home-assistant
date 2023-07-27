from assistant.listener import Listener
from utils.custom_logging import CustomLogging
from services.mqtt_service import MqttConfig, MqttService

logger = CustomLogging("logs/assistant.log")

class ListenerMqtt(Listener):
    mqtt_service: MqttService
    pending_commands: list
    
    def __init__(self, data_config: dict):
        mqtt_config = MqttConfig.from_json(data_config)
        self.mqtt_service = MqttService(mqtt_config, self.handle_command)
        self.pending_commands = []
        print(f"ListenerMqtt: {self.mqtt_service}")

    def handle_command(self, client, userdata, message):
        topicRecieved = message.topic
        messageRecieved = str(message.payload.decode("utf-8"))
        logger.info(f"[Topic]:{topicRecieved} | [Message Recieved]:{messageRecieved}")
        if(messageRecieved == "execute"):
            command = self.mqtt_service.get_command_from_topic(topicRecieved)
            if(command): self.pending_commands.append(command)

    def get_next_message(self) -> str:
        if(len(self.pending_commands)>0):
            return self.pending_commands.pop(0)
        return None