import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from message_handler import LLMMessageHandler
from web_search import WebSearchHandler

class RequestHandler(BaseHTTPRequestHandler):
    web_search_handler = WebSearchHandler(os.environ['SUBSCRIPTION_KEY'])
    llm_message_handler = LLMMessageHandler(os.environ['ANYSCALE_API_KEY'])
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data_bytes = self.rfile.read(content_length)
        post_data_str = post_data_bytes.decode("UTF-8")

        print(post_data_str)
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # Step 1 is to search the web
        myDict = RequestHandler.web_search_handler.web_search(post_data_str)
        
        url = [i for i in myDict.keys()]
        data = [s for s in myDict.values()]
        data_str = "".join(data)
        message = RequestHandler.llm_message_handler.handle_message(data_str)

        response = message['choices'][0]['message']['content'] + "\n" + url[0] + "\n" + url[1]

        self.wfile.write(bytes(response, "utf8"))

with HTTPServer(("localhost", 8000), RequestHandler) as server:
    server.serve_forever()