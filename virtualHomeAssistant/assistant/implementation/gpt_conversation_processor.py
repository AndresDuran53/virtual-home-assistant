from assistant.conversation_processor import ConversationProcessor
from utils.custom_logging import CustomLogging
from services.gpt_service import OpenAIGPT3
from utils.csv_storage import CSVStorage

logger = CustomLogging("logs/assistant.log")

class GPTConversationProcessor(ConversationProcessor):
    chat_service: OpenAIGPT3

    def __init__(self, data_config: dict) -> None:
            logger.info(f"Creating OpenAi GPT3 service...")
            self.chat_service = OpenAIGPT3.from_json(data_config)
            logger.info(f"Creating token manager...")
            self.token_manager = CSVStorage(self.chat_service.used_chars_filename)

    def can_send_new_message(self, message: str) -> bool:
        max_per_day = self.token_manager.get_value_for_date()
        logger.info(f"[Tokens used today]: {max_per_day}")
        return self.chat_service.can_do_question(message,max_per_day)

    def send_message(self, message: str, independent_message = False) -> dict:
        if(message == None and message == ""): return
        if(self.can_send_new_message(message)):
            logger.info("Sending request to openai api.")
            text_result,total_tokens = self.chat_service.welcome_home_chat(message,independent_message)
            logger.info(f"[GPT3 Response]: {text_result}")
            self.token_manager.increase_value_for_today_by(total_tokens)
            logger.info(f"[Total tokens used]: {total_tokens}")
            return text_result
        else:
            logger.error("Too many tokens to request.")
            return None