import { useState } from "react";
import {
      MinChatUiProvider,
      MainContainer,
      MessageInput,
      MessageContainer,
      MessageList,
      MessageHeader
    } from "@minchat/react-chat-ui";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Settings from './Settings';

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

  const [fileName, setFileName] = useState('');
  const [fullFilePath, setFullFilePath] = useState('');

  const uploadFile = (file) => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.click();

    fileInput.addEventListener('change', (event) => {
      console.log(event.target.files);
      const selectedFile = event.target.files[0];
      setFileName(selectedFile.name);
      setFullFilePath(selectedFile)
    });
  };

  const handleSubmit = (message) => {
    // Handle the message submission logic here
    console.log("Message submitted:", message);
    console.log("File Uploaded:", fileName)

    const formData = new FormData();
    if (fileName !== '') {
      formData.append('file', fullFilePath);
    }
    formData.append('query', message);

    fetch('http://localhost:8000', {
      method: 'POST',
      body: formData
    })
      .then(response => response.text())
      .then(data => {
        // Handle the response from the server
        console.log("Response from server:", data);
        setMessages(prevMessages => [
          ...prevMessages,
          {
            text: message.replace(/\/\w+/g, ''),
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
    <Router>
      <Routes>
        <Route path="/settings" element={<Settings />} />
        <Route path="/" element={
          <MinChatUiProvider theme="#6ea9d7">
            <MainContainer style={{ height: '100vh' }}>
              <MessageContainer>
                <MessageHeader />
                <MessageList
                  currentUserId='user'
                  messages={messages}
                />
                <input type="text" name="fileName" value={fileName} readOnly />
                <MessageInput placeholder="Ask a question or type '/' for commands" onSendMessage={handleSubmit} onAttachClick={uploadFile}/>
              </MessageContainer>
            </MainContainer>
          </MinChatUiProvider>
        } />
      </Routes>
    </Router>
  )
}

export default App

