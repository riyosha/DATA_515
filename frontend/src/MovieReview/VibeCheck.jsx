import { useState } from 'react';
import PropTypes from 'prop-types';
import './VibeCheck.css';

const VibeCheck = ({ filmUrl }) => {
  const [username, setUsername] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!username.trim()) {
      setError('Please enter a username');
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await fetch('/api/taste', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          film_url: filmUrl,
          username: username.trim(),
        }),
      });

      if (!res.ok) {
        throw new Error(`Error: ${res.status}`);
      }

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      console.error('Error fetching vibe check:', err);
      setError('Failed to get vibe check. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="vibe-check-container">
      <h2 className="vibe-check-title">Vibe check this movie</h2>

      <form onSubmit={handleSubmit} className="vibe-check-form">
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter letterboxd username"
          className="vibe-check-input"
          disabled={loading}
        />
        <button type="submit" className="vibe-check-button" disabled={loading}>
          {loading ? 'Checking...' : 'Submit'}
        </button>
      </form>

      {error && <div className="vibe-check-error">{error}</div>}

      {loading && (
        <div className="vibe-check-loading">Checking the vibes...</div>
      )}

      {response && (
        <div className="vibe-check-result">
          <h3 className="vibe-check-result-title">Results for {username}</h3>
          <div className="vibe-check-result-content">
            {response.taste ? (
              <p>{response.taste}</p>
            ) : (
              <p>No vibe match information available.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

// Add PropTypes validation
VibeCheck.propTypes = {
  filmUrl: PropTypes.string.isRequired,
};

export default VibeCheck;
