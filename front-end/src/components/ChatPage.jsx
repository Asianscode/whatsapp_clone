import React, { useState } from 'react';
import axios from 'axios';

const ChatPage = () => {
  const [selectedContact, setSelectedContact] = useState(null);
  const [messages, setMessages] = useState([]);

  const loadChat = async (contactId) => {
    try {
      const response = await axios.post('http://localhost:8000/load_chat/', { contact_id: contactId });
      setMessages(response.data.messages);
      setSelectedContact(contactId);
    } catch (error) {
      console.error('Error loading chat:', error);
    }
  };

  const sendMessage = async () => {
    try {
      await axios.post('http://localhost:8000/api/messages/', {
        content: messageContent,
        recipient: selectedContact,
      });
      setMessageContent('');  // Clear input field
      loadChat(selectedContact);  // Reload chat to include the new message
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div>
      <div className="chat-sidebar">
        {/* Sidebar with contacts will be here */}
      </div>
      <div className="chat-window">
        {/* Chat window */}
        {messages.map((message, index) => (
          <div key={index} className="message">
            <p>{message.content}</p>
          </div>
        ))}
        <input
          type="text"
          value={messageContent}
          onChange={(e) => setMessageContent(e.target.value)}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatPage;
