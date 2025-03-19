from utils.custom_logging import CustomLogging
from utils.configuration_reader import ConfigurationReader
from assistant.assistant import Assistant
from assistant.implementations.listener_mqtt import ListenerMqtt
from assistant.implementations.voice_mqtt import VoiceMqtt
from assistant.implementations.gpt_conversation_processor import GPTConversationProcessor
from controllers.decision_engine import DecisionMaker

logger = CustomLogging("logs/assistant.log")

def create_assistant(logger: CustomLogging, data_config: dict) -> Assistant:
    listener_mqtt = ListenerMqtt(data_config)
    voice_mqtt = VoiceMqtt(data_config)
    gpt_conversation_processor = GPTConversationProcessor(data_config)
    decision_maker = DecisionMaker(data_config)
    return Assistant(
        listener=listener_mqtt,
        voice=voice_mqtt,
        conversation_processor=gpt_conversation_processor,
        decision_maker=decision_maker,
        logger=logger,
        data_config=data_config,
    )

def main():
    logger.info("[STARTING SYSTEM] Initializing the system...")
    logger.info("Reading configuration file...")
    data_config = ConfigurationReader.read_config_file()
    assistant = create_assistant(logger, data_config)
    assistant.loop()

if __name__ == "__main__":
    main()