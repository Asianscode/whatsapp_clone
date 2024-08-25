// VideoCall.jsx
import React, { useRef, useState } from 'react';
import { io } from 'socket.io-client';

const VideoCall = ({ userId }) => {
  const [isCallActive, setIsCallActive] = useState(false);
  const localVideoRef = useRef(null);
  const remoteVideoRef = useRef(null);
  const peerConnection = useRef(null);
  const socket = useRef(null);

  const startCall = async () => {
    // Initialize WebRTC connection
    peerConnection.current = new RTCPeerConnection();

    // Get user media (video/audio)
    const localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    localVideoRef.current.srcObject = localStream;

    // Add local tracks to peer connection
    localStream.getTracks().forEach(track => {
      peerConnection.current.addTrack(track, localStream);
    });

    // Listen for remote tracks
    peerConnection.current.ontrack = event => {
      remoteVideoRef.current.srcObject = event.streams[0];
    };

    // Connect to the signaling server
    socket.current = io('http://your-signaling-server-url');

    // Send offer to the remote peer
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
    // Close the peer connection
    if (peerConnection.current) {
      peerConnection.current.close();
      peerConnection.current = null;
    }

    // Disconnect from the signaling server
    if (socket.current) {
      socket.current.disconnect();
      socket.current = null;
    }

    setIsCallActive(false);
  };

  return (
    <div className="video-call">
      <video ref={localVideoRef} autoPlay muted />
      <video ref={remoteVideoRef} autoPlay />
      <div className="controls">
        {!isCallActive && <button onClick={startCall}>Start Call</button>}
        {isCallActive && <button onClick={endCall}>End Call</button>}
      </div>
    </div>
  );
};

export default VideoCall;
