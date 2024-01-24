import openai
class LLMMessageHandler:
    def __init__(self, api_key):
        self.client = openai.OpenAI(base_url = "https://api.endpoints.anyscale.com/v1", api_key = api_key)
    
    def handle_message(self, message):
        chat_completion = self.client.chat.completions.create( model="meta-llama/Llama-2-70b-chat-hf",
                                                         messages=[{"role": "system", "content": "Summarize the given input in less than 100 words"}, 
                                                                   {"role": "user", "content": message }], temperature=0.7) 
        return chat_completion.model_dump()

