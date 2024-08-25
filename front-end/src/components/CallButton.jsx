// CallButton.jsx
import React from 'react';

const CallButton = ({ onStartCall, callType }) => {
  return (
    <button onClick={() => onStartCall(callType)}>
      {callType === 'video' ? 'Start Video Call' : 'Start Audio Call'}
    </button>
  );
};

export default CallButton;
