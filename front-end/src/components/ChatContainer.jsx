// ChatContainer.jsx
import React, { useState } from 'react';
import ChatInput from './ChatInput';
import VoiceRecorder from './VoiceRecorder';
import MessageList from './MessageList';

const ChatContainer = ({ userId }) => {
  const [messages, setMessages] = useState([]);

  const handleSendMessage = (newMessage) => {
    setMessages([...messages, newMessage]);
  };

  return (
    <div className="chat-container">
      <MessageList messages={messages} />
      <ChatInput userId={userId} onSendMessage={handleSendMessage} />
      <VoiceRecorder userId={userId} />
    </div>
  );
};

const styles = {
    chatContainer: {
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
    },
    chatInput: {
      display: 'flex',
      alignItems: 'center',
    },
    messageList: {
      flex: 1,
      overflowY: 'auto',
    },
  };
  
  // Usage in JSX
  <div style={styles.chatContainer}>
    <MessageList messages={messages} />
    <div style={styles.chatInput}>
      <ChatInput userId={userId} onSendMessage={handleSendMessage} />
      <VoiceRecorder userId={userId} />
    </div>
  </div>
  

export default ChatContainer;
