import React, { useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

const AccountCreationPage = () => {
  const { userId } = useParams();  // Get user ID from URL
  const navigate = useNavigate();  // For navigation after successful account creation
  const [username, setUsername] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [profilePicture, setProfilePicture] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!username || !phoneNumber || !profilePicture) {
      setError('All fields are required.');
      return;
    }

    const formData = new FormData();
    formData.append('username', username);
    formData.append('phone_number', phoneNumber);
    formData.append('profile_picture', profilePicture);

    try {
      await axios.post(`http://localhost:8000/account-creation/${userId}/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      // Redirect to home or another page after successful account creation
      navigate('/home');
    } catch (err) {
      console.error('Account creation failed:', err);
      setError('Account creation failed. Please try again.');
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.formContainer}>
        <h1 style={styles.heading}>Create Account</h1>
        {error && <p style={styles.error}>{error}</p>}
        <form onSubmit={handleSubmit}>
          <input 
            type="text" 
            placeholder="Username" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            style={styles.input} 
          />
          <input 
            type="text" 
            placeholder="Phone Number" 
            value={phoneNumber} 
            onChange={(e) => setPhoneNumber(e.target.value)} 
            style={styles.input} 
          />
          <input 
            type="file" 
            onChange={(e) => setProfilePicture(e.target.files[0])} 
            style={styles.input} 
          />
          <button 
            type="submit" 
            style={styles.button}
          >
            Create Account
          </button>
        </form>
      </div>
    </div>
  );
};

// Inline CSS for the AccountCreationPage component
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

export default AccountCreationPage;
