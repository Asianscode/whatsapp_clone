import React, { useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const OtpVerifyPage = () => {
  const { userId } = useParams();
  const [otp, setOtp] = useState('');
  const [error, setError] = useState('');

  const handleVerifyOtp = async () => {
    if (!otp) {
      setError('Please enter the OTP.');
      return;
    }

    try {
      await axios.post(`http://localhost:8000/otp-verify/${userId}/`, { otp });
      window.location.href = `/account-creation/${userId}`;
    } catch (err) {
      console.error('OTP verification failed:', err);
      setError('Invalid or expired OTP. Please try again.');
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.formContainer}>
        <h1 style={styles.heading}>Verify OTP</h1>
        {error && <p style={styles.error}>{error}</p>}
        <input 
          type="text" 
          placeholder="Enter OTP" 
          value={otp} 
          onChange={(e) => setOtp(e.target.value)} 
          style={styles.input} 
        />
        <button 
          onClick={handleVerifyOtp} 
          style={styles.button}
        >
          Verify OTP
        </button>
      </div>
    </div>
  );
};

// Inline CSS for the OtpVerifyPage component
const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    backgroundColor: '#f0f0f0',
  },
  formContainer: {
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 0 10px rgba(0,0,0,0.1)',
    backgroundColor: '#fff',
    width: '300px',
  },
  heading: {
    marginBottom: '20px',
    textAlign: 'center',
  },
  input: {
    width: '100%',
    padding: '10px',
    marginBottom: '10px',
    borderRadius: '4px',
    border: '1px solid #ddd',
    boxSizing: 'border-box',
  },
  button: {
    width: '100%',
    padding: '10px',
    borderRadius: '4px',
    border: 'none',
    backgroundColor: '#007bff',
    color: '#fff',
    fontSize: '16px',
    cursor: 'pointer',
  },
  error: {
    color: 'red',
    marginBottom: '10px',
    textAlign: 'center',
  }
};

export default OtpVerifyPage;

