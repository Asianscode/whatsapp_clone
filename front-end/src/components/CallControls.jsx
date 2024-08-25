// CallControls.jsx
import React from 'react';

const CallControls = ({ onEndCall, onToggleVideo, onToggleMute, isMuted, isVideoOn }) => {
  return (
    <div className="call-controls">
      <button onClick={onEndCall}>End Call</button>
      <button onClick={onToggleVideo}>
        {isVideoOn ? 'Turn Video Off' : 'Turn Video On'}
      </button>
      <button onClick={onToggleMute}>
        {isMuted ? 'Unmute' : 'Mute'}
      </button>
    </div>
  );
};

export default CallControls;
