## Just Another Chat Bot
The bot enables you to explore the web, condense information, and search through documents.

### Components
- Bot client - React App
- Bot Server - Written in python

### Dependencies
- @minchat/react-chat-ui
- Bing APIs SDK for Python
- AnyScale API
- ChromaDB (InMemory)

### General Internet Search

#### Workflow
1. The Client App initiates the query.
2. The query is transmitted to the backend, which queries the Bing API.
3. The backend subsequently generates a map of URLs and snippets, sending it to OpenAI/Llama for summarization.
4. The summarized response is then relayed back to the client app.

#### Demo
https://github.com/gtinside/just-another-chat-bot/assets/9381570/8ac80db1-01f7-43c5-a7cb-99d3ea977026

### Summarization
The three predominant methods of summarization include:

1. Directly extracting the data and forwarding it to LLM for summarization. While suitable for smaller documents, this approach becomes costly and encounters token limitations for larger documents.
2. Employing Langchain MapReduce to divide the document into segments, sending each part to LLM for summarization, and then consolidating the responses before sending them back to LLM for the final summary. Although easy to implement, this method exhibits high latency, requiring multiple invocations of LLM.
3. Utilizing K-means vector clustering, the approach implemented in this project involves the following steps:
    a. Segmenting the document into sections (paragraphs were used as sections in this case).
    b. Vectorizing each section.
    c. Employing K-means clustering to label and cluster the sections, with the number of clusters varying based on the document type.
    d. Identifying the representative chunk from each cluster.
    e. Combining all the representative chunks from different clusters.
    f. Sending the consolidated representative chunk to LLM for the final summary.

#### Workflow
1. The user submits a document in the application and requests summarization.
2. The document undergoes parsing and is stored temporarily.
3. The backend subsequently executes steps 3.a to 3.f outlined in the preceding section.

#### Demo
https://github.com/gtinside/just-another-chat-bot/assets/9381570/e892cc27-aef9-4e4e-a430-3e25aa60eb15



### Search within a document

#### Workflow
1. The user uploads a document in the application and submits a list of questions.
2. The document undergoes parsing and is stored temporarily.
3. The backend extracts text from the document and generates embeddings.
4. These embeddings are then stored in ChromaDB.
5. The submitted query is executed on the collection in ChromaDB.
6. The response is forwarded to LLM for the final summary, which is then sent back to the user.

#### Demo
