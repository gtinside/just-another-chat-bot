## Just Another Chat Bot
The bot will allow you to search the internet

### Components
- Bot client 
- Bot Server

### Workflow
1. User initiates the query via Client App
2. The query is sent to backend which queries Bing API
3. The backend then computes a map of URL and Snippet and send it to OpenAI/Llama for Summarization
4. The response is then sent back to the client app

### Dependencies
- @minchat/react-chat-ui
- Bing APIs SDK for Python
- AnyScale API

### Demo
![](Just-Another-Bot.mp4)
