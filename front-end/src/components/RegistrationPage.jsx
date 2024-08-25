import React, { useState } from 'react';
import axios from 'axios';

const RegistrationPage = () => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');

  const handleRegister = async () => {
    if (!email) {
      setError('Please enter an email address.');
      return;
    }

    try {
      await axios.post('http://localhost:8000/register/', { email });
      window.location.href = `/otp-verify/${email}`;
    } catch (err) {
      console.error('Registration failed:', err);
      setError('Registration failed. Please try again.');
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.formContainer}>
        <h1 style={styles.heading}>Register</h1>
        {error && <p style={styles.error}>{error}</p>}
        <input 
          type="email" 
          placeholder="Email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
          style={styles.input} 
        />
        <button 
          onClick={handleRegister} 
          style={styles.button}
        >
          Register
        </button>
      </div>
    </div>
  );
};

// Inline CSS for the RegistrationPage component
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

export default RegistrationPage;
