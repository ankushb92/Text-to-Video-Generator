import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [count, setCount] = useState(0);
  const [message, setMessage] = useState('');

  useEffect(() => {
    setMessage('React SPA running in Kubernetes!');
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>{message}</h1>
        <div className="counter-section">
          <p>Counter: {count}</p>
          <button onClick={() => setCount(count + 1)}>
            Increment
          </button>
          <button onClick={() => setCount(count - 1)}>
            Decrement
          </button>
          <button onClick={() => setCount(0)}>
            Reset
          </button>
        </div>
        <div className="info-section">
          <p>This is a single page React application</p>
          <p>Hostname: {window.location.hostname}</p>
          <p>Port: {window.location.port || '80'}</p>
        </div>
      </header>
    </div>
  );
}

export default App;