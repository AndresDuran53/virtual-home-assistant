import openai
from openai.error import OpenAIError
import tiktoken
from custom_logging import CustomLogging


class OpenAIGPT3:
    def __init__(self, api_key, model, max_tokens_per_requests_sended=500, max_tokens_per_requests_recieved=600, max_tokens_per_day=10000, used_chars_filename='tokensSended.log',initial_conversation=[]):
        self.api_key = api_key
        openai.api_key = api_key
        self.max_tokens_per_requests_sended = max_tokens_per_requests_sended
        self.max_tokens_per_requests_recieved = max_tokens_per_requests_recieved
        self.max_tokens_per_day = max_tokens_per_day
        self.used_chars_filename = used_chars_filename
        self.model = model
        self.encoding = tiktoken.encoding_for_model(self.model)
        self.initial_conversation = initial_conversation
        self.logger = CustomLogging("logs/assistant.log")
        
    def generate_conversation(self, conversation):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                max_tokens=self.max_tokens_per_requests_recieved,
                presence_penalty = 0.2,
                frequency_penalty = 0.5,
                temperature = 0.8,
                request_timeout=10,
                messages=conversation
            )
            self.logger.info("Response recieved")
            # Obtener respuesta de Davinci
            message = response.choices[0]["message"]["content"]
            total_tokens = response.usage["total_tokens"]
            return message,total_tokens
        except OpenAIError as e:
            if isinstance(e, openai.error.Timeout):
                self.logger.error(f"Timeout Error trying to create chat completion: {e}")
            else:
                self.logger.error(f"OpenAIError Error trying to create chat completion: {e}")
            return "There is an issue with the artificial intelligence language model.",0
        except e:
            self.logger.error(f"Unexpected Error trying to create chat completion: {e}")
            return "There is an issue with the artificial intelligence language model.",0
            
    def count_token_amount(self,prompt):
        num_tokens = len(self.encoding.encode(prompt))
        return num_tokens
    
    def count_initial_conversation(self):
        input_count = 0
        for message in self.initial_conversation:
            input_count += self.count_token_amount(message["content"])
        return input_count
    
    def can_do_question(self,user_input,max_per_day):
        input_count = self.count_token_amount(user_input)
        input_count += self.count_initial_conversation()
        if(input_count>self.max_tokens_per_requests_sended): return False
        if(input_count+max_per_day>self.max_tokens_per_day): return False
        return True

    def welcome_home_chat(self,user_input):
        conversation = self.initial_conversation[:]
        conversation += [{"role": "user", "content": user_input}]
        self.logger.debug(f"Conversation Created: {conversation}")
        text_result,total_tokens = self.generate_conversation(conversation)
        return text_result,total_tokens

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