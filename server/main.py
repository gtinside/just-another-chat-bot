import os
import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer
from handlers.message_handler import LLMMessageHandler
from handlers.web_search import WebSearchHandler
from handlers.summary_generator import SummaryGenerator
from intent.intent_classifier import Command, IntentClassifier,Intent
from embeddings.embeddings_handler import EmbeddingsHandler
from db.persistence import Persistence, EventType

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

        #TODO: Separate the request by having different endpoints for different requests
        if self.path == '/upload':
            form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type']}
            )
            # To make this resillient, copy all the files to local directory 
            requestId = form['requestId'].value
            dir = f'/tmp/{requestId}/'
            for fileitem in form['file']:
                try:
                    if fileitem.file and fileitem.filename:
                        file= fileitem.file
                        filepath = dir + fileitem.filename.split("/")[-1]
                        dirpath = os.path.dirname(filepath)
                        os.makedirs(dirpath, exist_ok=True)
                        with open(filepath, 'wb') as f:
                            f.write(file.read())
                        Persistence.create_event(fileitem.filename, EventType.UPLOAD, username="admin")
                except Exception as e:
                    print(f'Error processing file {fileitem.filename} - {e}')
                
            # Once all the files are copied, we can start processing the files
            self.embeddings_handler.embed_documents(dir)
            # Remove the directory
            os.system(f'rm -rf {dir}')
            self.wfile.write(bytes("Files uploaded successfully, use command /search to query the data", "utf8"))
        else:
            # request for everything thing else
            # Parse the form data posted        
            form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type']}
            )

            # Access form data
            filepath = None
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

            # Step 1 is to idenity the type of query and then command
            command_type:Command = RequestHandler.intent_classifier.classify_command_type(query)
            try:
                if filepath:
                    message = RequestHandler.summary_generator.generate_summary(filepath)
                    summary = RequestHandler.llm_message_handler.handle_summarization(message)
                    response_on_summary = RequestHandler.llm_message_handler.handle_query_on_summary(summary['choices'][0]['message']['content'], query)
                    response = response_on_summary['choices'][0]['message']['content']
                    self.wfile.write(bytes(response, "utf8"))
                elif command_type == Command.SEARCH_EMBEDDINGS:
                    response = RequestHandler.embeddings_handler.query_embeddings(query)
                    self.wfile.write(bytes(str(response), "utf8"))
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