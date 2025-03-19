from utils.custom_logging import CustomLogging
from utils.configuration_reader import ConfigurationReader
from assistant.assistant import Assistant
from assistant.implementations.listener_mqtt import ListenerMqtt
from assistant.implementations.voice_mqtt import VoiceMqtt
from assistant.implementations.gpt_conversation_processor import GPTConversationProcessor
from whisper_transcribe.speech_handler import SpeechHandler
from controllers.decision_maker import DecisionMaker


logger = CustomLogging("logs/assistant.log")

def create_assistant(logger, data_config: dict):
    listener_mqtt = ListenerMqtt(data_config)
    #listener_stt = SpeechHandler()
    voice_mqtt = VoiceMqtt(data_config)
    gpt_conversation_processor = GPTConversationProcessor(data_config)
    decision_maker = DecisionMaker(data_config)
    assistant = Assistant(listener = listener_mqtt, 
                          voice = voice_mqtt, 
                          conversation_processor = gpt_conversation_processor,
                          decision_maker = decision_maker,
                          logger=logger, data_config=data_config)
    return assistant

def main():
    logger.info(f"[STARTING SYSTEM] Initializing the system...")
    logger.info(f"Reading configuration file...")
    data_config = ConfigurationReader.read_config_file()
    assistant = create_assistant(logger,data_config)
    assistant.loop()

if __name__ == "__main__":
    main()