import { useLocation, useNavigate } from 'react-router-dom';

const Roast = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { searchQuery } = location.state || { searchQuery: '' };

  return (
    <div className="roast-container">
      <header>
        <button onClick={() => navigate('/')}>Back to Home</button>
        <h1>Letterboxd Roast</h1>
      </header>

      <div className="roast-content">
        <p>
          Generating roast for: <strong>{searchQuery}</strong>
        </p>
        {/* Roast content will go here */}
      </div>
    </div>
  );
};

export default Roast;
