import { useState } from "react";
import {
      MinChatUiProvider,
      MainContainer,
      MessageInput,
      MessageContainer,
      MessageList,
      MessageHeader
    } from "@minchat/react-chat-ui";

function App() {
  const [messages, setMessages] = useState([
    {
      text: 'How can I help you?',
      user: {
        id: 'bot',
        name: 'D-Bot',
      },
    }
  ]);

  const handleSubmit = (message) => {
    // Handle the message submission logic here
    console.log("Message submitted:", message);

    fetch('http://localhost:8000', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({ message })
    })
      .then(response => response.text())
      .then(data => {
        // Handle the response from the server
        console.log("Response from server:", data);
        setMessages(prevMessages => [
          ...prevMessages,
          {
            text: message,
            user: {
              id: 'user',
              name: 'You',
            },
          },
          {
            text: data,
            user: {
              id: 'bot',
              name: 'D-Bot',
            },
          }
        ]);
      })
      .catch(error => {
        // Handle any errors that occur during the request
        console.error("Error:", error);
      });
  };

  return (
    <MinChatUiProvider theme="#6ea9d7">
      <MainContainer style={{ height: '100vh' }}>
        <MessageContainer>
          <MessageHeader />
          <MessageList
            currentUserId='user'
            messages={messages}
          />
          <MessageInput placeholder="Type message here" onSendMessage={handleSubmit}/>
        </MessageContainer>
      </MainContainer>
    </MinChatUiProvider>
  )
}

export default App

