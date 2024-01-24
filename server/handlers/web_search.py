from web_search_client import WebSearchClient
from azure.core.credentials import AzureKeyCredential
from collections import defaultdict

class WebSearchHandler:
    def __init__(self, subscription_key) -> None:
        self.subscription_key = subscription_key
        self.endpoint = "https://api.bing.microsoft.com"+  "/v7.0/"
        self.client = WebSearchClient(AzureKeyCredential(self.subscription_key))
    
    def web_search(self, query):
        data = self.client.web.search(query=query, answer_count=5)
        dataDict = defaultdict(str)
        for v in data.web_pages.value:
            dataDict[v.url] = v.snippet
        print(len(dataDict))
        return dataDict