from utils.custom_logging import CustomLogging
from utils.configuration_reader import ConfigurationReader
from assistant.assistant import Assistant
from assistant.implementation.listener_mqtt import ListenerMqtt
from assistant.implementation.voice_mqtt import VoiceMqtt
from assistant.implementation.gpt_conversation_processor import GPTConversationProcessor
from whisper_transcribe.speech_handler import SpeechHandler


logger = CustomLogging("logs/assistant.log")

def create_assistant(logger, data_config: dict):
    listener_mqtt = ListenerMqtt(data_config)
    listener_stt = SpeechHandler()
    listener_stt.execute()
    voice_mqtt = VoiceMqtt(data_config)
    gpt_conversation_processor = GPTConversationProcessor(data_config)
    assistant = Assistant(listener=listener_stt, voice=voice_mqtt, conversation_processor=gpt_conversation_processor,
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