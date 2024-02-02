import os
import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer
from message_handler import LLMMessageHandler
from web_search import WebSearchHandler
from summary_generator import SummaryGenerator
from intent_classifier import IntentClassifier,Intent
from embeddings_handler import EmbeddingsHandler

class RequestHandler(BaseHTTPRequestHandler):
    web_search_handler = WebSearchHandler(os.environ['SUBSCRIPTION_KEY'])
    llm_message_handler = LLMMessageHandler(os.environ['ANYSCALE_API_KEY'])
    intent_classifier = IntentClassifier(llm_message_handler)
    summary_generator = SummaryGenerator()
    embeddings_handler = EmbeddingsHandler()

    def do_OPTIONS(self):    
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()
        
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        form = cgi.FieldStorage(
        fp=self.rfile,
        headers=self.headers,
        environ={'REQUEST_METHOD': 'POST',
                 'CONTENT_TYPE': self.headers['Content-Type']}
        )

        # Access form data
        filepath = None
        query = None
        if 'file' in form:
            fileitem = form['file']
            if fileitem.file:
                file = fileitem.file
                filepath = '/tmp/' + fileitem.filename
                with open(filepath, 'wb') as f:
                    f.write(file.read())
            fileitem = form['file']
            if fileitem.file:
                file = fileitem.file
                
        if 'query' in form:
            query = form['query'].value

        # Step 1 is to idenity the type of request
        try:
            if filepath:
                message = RequestHandler.summary_generator.generate_summary(filepath)
                summary = RequestHandler.llm_message_handler.handle_summarization(message)
                response_on_summary = RequestHandler.llm_message_handler.handle_query_on_summary(summary['choices'][0]['message']['content'], query)
                response = response_on_summary['choices'][0]['message']['content']
                self.wfile.write(bytes(response, "utf8"))
            else:
                myDict = RequestHandler.web_search_handler.web_search(query)
                url = [i for i in myDict.keys()]
                data = [s for s in myDict.values()]
                data_str = "".join(data)
                message = RequestHandler.llm_message_handler.handle_message(data_str)

                response = message['choices'][0]['message']['content'] + "\n" + url[0] + "\n" + url[1]

                self.wfile.write(bytes(response, "utf8"))
        except ValueError:
            self.wfile.write(bytes("No results found, try again", "utf8"))
            return

with HTTPServer(("localhost", 8000), RequestHandler) as server:
    server.serve_forever()