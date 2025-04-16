from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion, Choice
import tiktoken
from utils.custom_logging import CustomLogging
from services.conversation_log import ConversationLog

class OpenAIGPT3:
    model: str

    def __init__(self, api_key, model, max_tokens_per_requests_sended=500, max_tokens_per_requests_recieved=600, max_tokens_per_day=10000, used_chars_filename='tokensSended.log',initial_conversation=[]):
        self.logger = CustomLogging("logs/assistant.log")
        self.api_key = api_key
        self.client = OpenAI(
            api_key=api_key
        )
        self.max_tokens_per_requests_sended = max_tokens_per_requests_sended
        self.max_tokens_per_requests_recieved = max_tokens_per_requests_recieved
        self.max_tokens_per_day = max_tokens_per_day
        self.used_chars_filename = used_chars_filename
        self.model = model
        try:
            self.encoding = tiktoken.encoding_for_model(self.model)
        except:
            self.logger.error(f"Tiktoken was not able to found the model: {self.model}")
            self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.initial_conversation: list = initial_conversation
        self.conversation_log = ConversationLog()
    
    def _count_initial_conversation(self) -> int:
        input_count = 0
        for message in self.initial_conversation:
            input_count += self._count_token_amount(message["content"])
        return input_count

    def _count_token_amount(self, prompt) -> int:
        num_tokens = len(self.encoding.encode(prompt))
        return num_tokens

    def _call_chat_completions(self, conversation) -> tuple[ChatCompletion | None, str]:
        attempt_counter=0
        _error = None
        while(attempt_counter<3):
            try:
                attempt_counter+=1
                timeout_aux = attempt_counter*20
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    max_tokens=self.max_tokens_per_requests_recieved,
                    presence_penalty = 0.2,
                    frequency_penalty = 0.5,
                    temperature = 0.8,
                    timeout=timeout_aux,
                    messages=conversation
                )
                return response,''
            except Exception as error:
                self.logger.error(f"Unexpected Error trying to create chat completion (attempt_counter {attempt_counter}: {error}")
        _error = "There is an issue with the artificial intelligence language model."
        return None,_error
    
    def _request_response(self, conversation) -> tuple[str, int]:
        total_tokens = 0
        response,_error = self._call_chat_completions(conversation)
        if(not response):
            return _error,total_tokens
        self.logger.info("Response recieved")
        message = response.choices[0].message.content
        if(not message): message = ''
        if response.usage is not None:
            total_tokens = response.usage.total_tokens
        else:
            total_tokens = self.max_tokens_per_requests_recieved
        return message,total_tokens
    
    def can_process_requests(self, user_input, max_per_day) -> bool:
        input_count = self._count_token_amount(user_input)
        input_count += self._count_initial_conversation()
        if (input_count > self.max_tokens_per_requests_sended): 
            return False
        if ((input_count + max_per_day) > self.max_tokens_per_day):
            return False
        return True
    
    def send_message(self, user_input: str, is_independent: bool = True) -> tuple[str, int]:
        conversation = self._prepare_conversation(user_input, is_independent)
        self.logger.debug(f"Conversation to send: {conversation}")
        text_response,total_tokens = self._request_response(conversation)
        if not is_independent:
            self.conversation_log.new_message("assistant", text_response)
        return text_response,total_tokens
    
    def _prepare_conversation(self, user_input, is_independent):
        if is_independent:
            conversation = self.initial_conversation.copy()
            conversation.append({"role": "user", "content": user_input})
        else:
            conversation = self.conversation_log.get_entries_as_dicts()
            if not conversation:
                self.logger.info("No chat history found. Starting a new conversation.")
                for message in self.initial_conversation:
                    self.conversation_log.new_message(message["role"], message["content"])
            self.conversation_log.new_message("user", user_input)
            conversation = self.conversation_log.get_entries_as_dicts()
        return conversation

    @classmethod
    def from_json(cls, json_config):
        config = json_config["openai"]
        api_key = config['apiKey']
        model = config['model']
        max_tokens_per_requests_sended = int(config['maxTokensPerRequestsSended'])
        max_tokens_per_requests_recieved = int(config['maxTokensPerRequestsRecieved'])
        max_tokens_per_day = int(config['maxTokensPerDay'])
        used_chars_filename = config['usedCharsFilename']
        initial_conversation = config['initialConversation']
        return OpenAIGPT3(api_key,model,max_tokens_per_requests_sended,max_tokens_per_requests_recieved,max_tokens_per_day,used_chars_filename,initial_conversation)