import openai

class LLMMessageHandler:
    def __init__(self, api_key):
        self.client = openai.OpenAI(base_url="https://api.endpoints.anyscale.com/v1", api_key=api_key)
        self.model = "meta-llama/Llama-2-70b-chat-hf"
    
    def handle_message(self, message):
        return self.generic_handler(system_prompt="Summarize the given input in less than 20 words", message=message)
    
    def handle_summarization(self, message):
        return self.generic_handler(system_prompt="Given a set of paragraphs, summarize the main ideas and key information concisely. Provide a coherent and informative summary that captures the essential points of the text. Ensure clarity, brevity, and accuracy in the summary.", message=message)

    def handle_intent_classification(self, message, intents):
        return self.generic_handler(system_prompt=f"Given the input message, determine its intent category. If the message explicitly requests a summary of the document, respond with 'SUMMARIZATION'; otherwise, respond with 'GENERAL'. Do not provide additional commentary.", message=message)

    def generic_handler(self, system_prompt, message):
        chat_completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7
        )
        return chat_completion.model_dump()



