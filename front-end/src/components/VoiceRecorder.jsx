// VoiceRecorder.jsx
import React, { useState } from 'react';
import axios from 'axios';

const VoiceRecorder = ({ userId }) => {
  const [recording, setRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);

  const startRecording = () => {
    setRecording(true);
    // Logic to start recording audio
  };

  const stopRecording = () => {
    setRecording(false);
    // Logic to stop recording and create a blob
    setAudioBlob(/* Audio blob from recording */);
  };

  const handleSendVoice = async () => {
    if (audioBlob) {
      const formData = new FormData();
      formData.append('file', audioBlob);

      try {
        const response = await axios.post(`http://your-backend-url/upload-voice/${userId}/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        if (response.data.status === 'success') {
          // Handle successful voice message upload
          setAudioBlob(null);
        }
      } catch (error) {
        console.error('Error sending voice message:', error);
      }
    }
  };

  return (
    <div className="voice-recorder">
      {recording ? (
        <button onClick={stopRecording}>Stop</button>
      ) : (
        <button onClick={startRecording}>Record</button>
      )}
      {audioBlob && (
        <button onClick={handleSendVoice}>Send Voice Message</button>
      )}
    </div>
  );
};

export default VoiceRecorder;
