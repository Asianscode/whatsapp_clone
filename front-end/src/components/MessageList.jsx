// MessageList.jsx
import React from 'react';

const MessageList = ({ messages }) => {
  return (
    <div className="message-list">
      {messages.map((message, index) => (
        <div key={index} className="message">
          {message.text && <p>{message.text}</p>}
          {message.media && (
            <img src={message.media} alt="Media" />
          )}
          {message.voice && (
            <audio controls src={message.voice}></audio>
          )}
        </div>
      ))}
    </div>
  );
};

export default MessageList;
