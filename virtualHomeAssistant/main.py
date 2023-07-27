from utils.custom_logging import CustomLogging
from utils.configuration_reader import ConfigurationReader
from assistant.assistant import Assistant
from assistant.listener_mqtt import ListenerMqtt
from assistant.conversation_processor import ConversationProcessor
from assistant.voice import Voice

logger = CustomLogging("logs/assistant.log")

def create_assistant(logger, data_config: dict):
    listener_mqtt = ListenerMqtt(data_config)
    assistant = Assistant(listener=listener_mqtt, logger=logger, data_config=data_config)
    return assistant

def main():
    logger.info(f"[STARTING SYSTEM] Initializing the system...")
    logger.info(f"Reading configuration file...")
    data_config = ConfigurationReader.read_config_file()
    assistant = create_assistant(logger,data_config)
    assistant.loop()

if __name__ == "__main__":
    main()