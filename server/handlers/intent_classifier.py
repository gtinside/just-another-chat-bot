from message_handler import LLMMessageHandler
from enum import Enum

class Intent(Enum):
    SUMMARIZATION = "SUMMARIZATION"
    GENERAL = "GENERAL"

class IntentClassifier:
    def __init__(self, llm_message_handler:LLMMessageHandler, intents:set=(Intent.SUMMARIZATION, Intent.GENERAL)) -> None:
        self.intents = intents
        self.llm_message_handler = llm_message_handler
    
    def classify_intent(self, message:str) -> str:
        response= self.llm_message_handler.handle_intent_classification(message, self.intents)
        for intent in self.intents:
            if intent.value == str(response['choices'][0]['message']['content']).strip():
                return intent
        

        