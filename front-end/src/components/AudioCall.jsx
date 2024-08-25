// AudioCall.jsx
import React, { useRef, useState } from 'react';
import { io } from 'socket.io-client';

const AudioCall = ({ userId }) => {
  const [isCallActive, setIsCallActive] = useState(false);
  const remoteAudioRef = useRef(null);
  const peerConnection = useRef(null);
  const socket = useRef(null);

  const startCall = async () => {
    peerConnection.current = new RTCPeerConnection();

    const localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    localStream.getTracks().forEach(track => {
      peerConnection.current.addTrack(track, localStream);
    });

    peerConnection.current.ontrack = event => {
      remoteAudioRef.current.srcObject = event.streams[0];
    };

    socket.current = io('http://your-signaling-server-url');

    const offer = await peerConnection.current.createOffer();
    await peerConnection.current.setLocalDescription(offer);
    socket.current.emit('call-user', { userId, offer });

    socket.current.on('call-accepted', async ({ answer }) => {
      await peerConnection.current.setRemoteDescription(new RTCSessionDescription(answer));
      setIsCallActive(true);
    });

    socket.current.on('call-ended', () => {
      endCall();
    });
  };

  const endCall = () => {
    if (peerConnection.current) {
      peerConnection.current.close();
      peerConnection.current = null;
    }
    if (socket.current) {
      socket.current.disconnect();
      socket.current = null;
    }
    setIsCallActive(false);
  };

  return (
    <div className="audio-call">
      <audio ref={remoteAudioRef} autoPlay />
      <div className="controls">
        {!isCallActive && <button onClick={startCall}>Start Call</button>}
        {isCallActive && <button onClick={endCall}>End Call</button>}
      </div>
    </div>
  );
};

export default AudioCall;
