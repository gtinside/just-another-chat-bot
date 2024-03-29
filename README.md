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
- OpenAI (the key needs to be set)

### How to?
- Run client locally,  
```
cd client
npm start
```
- Run server locally (recommended to use launch.json)
```
python3 main.py
```


### Functionalities
- General Internet Search
- File Summarization
- Search within a document
- Semantic search on multiple documents

### General Internet Search

#### Workflow
1. The Client App initiates the query.
2. The query is transmitted to the backend, which queries the Bing API.
3. The backend subsequently generates a map of URLs and snippets, sending it to OpenAI/Llama for summarization.
4. The summarized response is then relayed back to the client app.

#### Demo
https://github.com/gtinside/just-another-chat-bot/assets/9381570/8ac80db1-01f7-43c5-a7cb-99d3ea977026

### File Summarization
The three predominant methods of summarization include:

1. Directly extracting the data and forwarding it to LLM for summarization. While suitable for smaller documents, this approach becomes costly and encounters token limitations for larger documents.
2. Employing Langchain MapReduce to divide the document into segments, sending each part to LLM for summarization, and then consolidating the responses before sending them back to LLM for the final summary. Although easy to implement, this method exhibits high latency, requiring multiple invocations of LLM.
3. Utilizing K-means vector clustering, the approach implemented in this project involves the following steps:
    - Segmenting the document into sections (paragraphs were used as sections in this case).
    - Vectorizing each section.
    - Employing K-means clustering to label and cluster the sections, with the number of clusters varying based on the document type.
    - Identifying the representative chunk from each cluster.
    - Combining all the representative chunks from different clusters.
    - Sending the consolidated representative chunk to LLM for the final summary.

#### Workflow
1. The user submits a document in the application and requests summarization.
2. The document undergoes parsing and is stored temporarily.
3. The backend subsequently executes steps 3.a to 3.f outlined in the preceding section.

#### Demo
https://github.com/gtinside/just-another-chat-bot/assets/9381570/5578c91a-e042-4a4c-875d-003e4d4b2292

### Search within a document

#### Workflow
1. The user uploads a document in the application and submits a list of questions.
2. The document undergoes parsing and is stored temporarily.
3. The backend extracts text from the document and generates embeddings.
4. The document is clustered using K-Means clustering.
5. The representative chunks for each cluster are sent to LLM for summarization.
5. User input query and the summay is sent to LLM to get the final answer, which is then sent back to user.

#### Demo
https://github.com/gtinside/just-another-chat-bot/assets/9381570/7cced996-f0ca-48dc-8c15-8f95c7a22855

### Semantic search on multiple documents

#### Workflow
1. The user navigates to settings page and upload the directory with files in it.
2. File events are created in SQLite Events table 
3. The server process the files and do the following:
    a. Chunking - 100 chunks per file
    b. Associate metadata with each chunk
    c. Generate and store embeddings in chromadb

#### Demo


### pip errors
```
source venv/bin/activate
pip freeze | xargs pip uninstall -y
pip install llama-index
```

### TODO
1. Better exception handling specially in main.py and handlers package
2. Implement intent classifier for query and command using Instructor
3. Improve deployment strategy
4. Apply stylesheet to Settings page
