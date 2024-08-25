// ChatInput.jsx
import React, { useState } from 'react';
import axios from 'axios';

const ChatInput = ({ userId, onSendMessage }) => {
  const [message, setMessage] = useState('');
  const [media, setMedia] = useState(null);

  const handleInputChange = (e) => {
    setMessage(e.target.value);
  };

  const handleMediaChange = (e) => {
    setMedia(e.target.files[0]);
  };

  const handleSend = async () => {
    const formData = new FormData();
    formData.append('message', message);
    if (media) {
      formData.append('file', media);
    }

    try {
      const response = await axios.post(`http://your-backend-url/send-message/${userId}/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      if (response.data.status === 'success') {
        onSendMessage(response.data.message);
        setMessage('');
        setMedia(null);
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="chat-input">
      <input 
        type="text" 
        value={message} 
        onChange={handleInputChange} 
        placeholder="Type a message" 
      />
      <input 
        type="file" 
        onChange={handleMediaChange} 
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
};

export default ChatInput;
