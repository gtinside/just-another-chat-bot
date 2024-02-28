import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.indices.service_context import ServiceContext
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter

class EmbeddingsHandler:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("documents")
        self.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
    
    def embed_documents(self, doc_location):
        """
        Process the document by performing the following steps:
        1. Read the document.
        2. Set up ChromaVectorStore and load in data.
        3. Create a VectorStoreIndex from the documents using the specified storage context, embed model, and service context.
        """
        service_context = ServiceContext.from_defaults(chunk_size=100, chunk_overlap=10)
        documents = SimpleDirectoryReader(doc_location).load_data()

        vector_store = ChromaVectorStore(chroma_collection=self.collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        self.index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, embed_model=self.embed_model, service_context=service_context
        )

    def query_embeddings(self, query, num_of_results=5):
        query = self.embeddings.embed_query(query)
        return self.collection.query(query_embeddings=[query], n_results=num_of_results)
       