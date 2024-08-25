// CallContainer.jsx
import React, { useState, useRef } from 'react';
import CallButton from './CallButton';
import CallControls from './CallControls';
import VideoPlayer from './VideoPlayer';

const CallContainer = ({ userId, signalingServerUrl }) => {
  const [isInCall, setIsInCall] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [isVideoOn, setIsVideoOn] = useState(true);
  const [localStream, setLocalStream] = useState(null);
  const [remoteStream, setRemoteStream] = useState(null);

  const peerConnectionRef = useRef(null);

  const startCall = async (callType) => {
    try {
      // Get local media stream
      const constraints = {
        video: callType === 'video',
        audio: true,
      };
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      setLocalStream(stream);

      // Initialize WebRTC peer connection
      const peerConnection = new RTCPeerConnection();
      peerConnectionRef.current = peerConnection;

      // Add local stream tracks to peer connection
      stream.getTracks().forEach(track => {
        peerConnection.addTrack(track, stream);
      });

      // Handle incoming remote stream
      peerConnection.ontrack = (event) => {
        setRemoteStream(event.streams[0]);
      };

      // Set up signaling (negotiation, ICE candidate exchange, etc.)
      // You need to implement signaling logic here (e.g., using WebSocket)

      setIsInCall(true);
    } catch (error) {
      console.error('Error starting call:', error);
    }
  };

  const endCall = () => {
    if (peerConnectionRef.current) {
      peerConnectionRef.current.close();
      peerConnectionRef.current = null;
    }
    setLocalStream(null);
    setRemoteStream(null);
    setIsInCall(false);
  };

  const toggleMute = () => {
    if (localStream) {
      localStream.getAudioTracks().forEach(track => {
        track.enabled = !track.enabled;
      });
      setIsMuted(!isMuted);
    }
  };

  const toggleVideo = () => {
    if (localStream) {
      localStream.getVideoTracks().forEach(track => {
        track.enabled = !track.enabled;
      });
      setIsVideoOn(!isVideoOn);
    }
  };

  return (
    <div className="call-container">
      {!isInCall ? (
        <div className="call-buttons">
          <CallButton onStartCall={startCall} callType="video" />
          <CallButton onStartCall={startCall} callType="audio" />
        </div>
      ) : (
        <>
          <VideoPlayer localStream={localStream} remoteStream={remoteStream} />
          <CallControls
            onEndCall={endCall}
            onToggleVideo={toggleVideo}
            onToggleMute={toggleMute}
            isMuted={isMuted}
            isVideoOn={isVideoOn}
          />
        </>
      )}
    </div>
  );
};

export default CallContainer;
