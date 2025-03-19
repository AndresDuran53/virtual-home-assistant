import os
import sys

here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '..'))

from utils.configuration_reader import ConfigurationReader
from assistant.implementations.gpt_conversation_processor import GPTConversationProcessor

def main():
    print("Starting test")
    data_config = ConfigurationReader.read_config_file()
    gpt_conversation_processor = GPTConversationProcessor(data_config)
    result = gpt_conversation_processor.send_message("Sabes mi nombre?",True)
    print(result)

if __name__ == "__main__":
    main()