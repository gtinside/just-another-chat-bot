import re
import textract
from sklearn.cluster import KMeans
from scipy.spatial import distance
from langchain_community.embeddings import HuggingFaceEmbeddings

class SummaryGenerator:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings()
    
    def generate_summary(self, file):
        # Step 1: is to split the document into sections, textract returuns the text as byte, hence decoding it to utf-8
        text = textract.process(file).decode('utf-8')
        # using 4 space as paragraph delimiter
        paragraphs = re.split('\n\s*', text)
        metadata = [{'source': file}] * len(paragraphs)

        # Step 2: is to generate embeddings for each paragraph   
        paragraph_embeddings = self.embeddings.embed_documents(paragraphs)     

        # Step 3: is to cluster the paragraphs and select the most representative paragraph from each cluster
        kmeans = KMeans(n_clusters=4).fit(paragraph_embeddings)
        cluster_labels = kmeans.labels_
        representative_paragraphs = []
        for i in range(4):
            cluster = [paragraphs[j] for j in range(len(paragraphs)) if cluster_labels[j] == i]
            cluster_embeddings = [paragraph_embeddings[j] for j in range(len(paragraphs)) if cluster_labels[j] == i]
            cluster_center = kmeans.cluster_centers_[i]
            representative_paragraphs.append(cluster[distance.cdist([cluster_center], cluster_embeddings).argmin()])

        # Step 4: order paragraphs based on their occurrence in the text
        ordered_paragraphs = sorted(representative_paragraphs, key=lambda p: text.index(p))

        #Step 5: Combine the paragraph and send to LLM for summarization
        input = ".".join(ordered_paragraphs) 
        print(input)
        return input
            
