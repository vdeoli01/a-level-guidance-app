import React, { useState, useEffect } from 'react';
import './App.css';

const BASE_API_ENDPOINT = process.env.REACT_APP_BASE_API_ENDPOINT;

function App() {
  const [message, setMessage] = useState('');
  console.log(process.env.REACT_APP_BASE_API_ENDPOINT);
  console.log(process.env.NODE_ENV)
  useEffect(() => {
    fetch(BASE_API_ENDPOINT)  // Adjust the URL to point to your backend endpoint.
        .then(response => response.json())
        .then(data => setMessage(data.message));
  }, []);

  return (
      <div className="App">
        <header className="App-header">
          {message}
        </header>
      </div>
  );
}

export default App;
