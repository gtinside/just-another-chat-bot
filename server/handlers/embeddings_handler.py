import uuid
import re
import chromadb
import textract
from langchain_community.embeddings import HuggingFaceEmbeddings

class EmbeddingsHandler:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings()
        chromadb_client = chromadb.Client()
        self.collection = chromadb_client.create_collection("uploads")
    
    def embed_documents(self, file):
        try:
            # Step 1: Split the document into sentences
            text = textract.process(file).decode('utf-8')
            # using 4 space as paragraph delimiter
            lines = re.split('\n', text)
            metadata = [{'source': file}] * len(lines)
            ids = [str(uuid.uuid4()) for i in range(len(lines))]  # Fix: Added missing square brackets

            # Step 2: is to generate embeddings for each line   
            line_embeddings = self.embeddings.embed_documents(lines)
            self.collection.add(documents=lines, embeddings=line_embeddings, metadatas=metadata, ids=ids)
        except Exception as e:
            print(e)
            raise ValueError("Error in embedding the document")

    def query_embeddings(self, query, file, num_of_results=5):
        return self.collection.query(query_texts=[query], n_results=num_of_results, where={"source": file})
       