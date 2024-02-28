from handlers.message_handler import LLMMessageHandler
from enum import Enum

class Intent(Enum):
    SUMMARIZATION = "SUMMARIZATION"
    GENERAL = "GENERAL"

class Command(Enum):
    SEARCH_EMBEDDINGS = "SEARCH_EMBEDDINGS"
    INTERNET_SEARCH = "INTERNET_SEARCH"

class IntentClassifier:
    def __init__(self, llm_message_handler:LLMMessageHandler, intents:set=(Intent.SUMMARIZATION, Intent.GENERAL)) -> None:
        self.intents = intents
        self.llm_message_handler = llm_message_handler
    
    def classify_query_type(self, query:str) -> Intent:
            """
            Classifies the query type - SUMMARIZATION or GENERAL based on the given message.

            Args:
                message (str): The message to be classified.

            Returns:
                str: The classified query type.

            """
            response= self.llm_message_handler.handle_intent_classification(query, self.intents)
            for intent in self.intents:
                if intent.value == str(response['choices'][0]['message']['content']).strip():
                    return intent
    
    def classify_command_type(self, query):
         if '/search' in query:
             return Command.SEARCH_EMBEDDINGS
         else:
              return Command.INTERNET_SEARCH
    
        

        