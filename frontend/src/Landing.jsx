import { useEffect, useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import './Landing.css';

const Landing = () => {
  const navigate = useNavigate();
  const placeholders = useMemo(
    () => [
      'Enter a letterboxd url...',
      'Should you really watch that movie?',
      'Enter your letterboxd username...',
      "I won't be too harsh, I promise...",
      "Just kidding, I'm going to be brutal",
    ],
    []
  );

  const [displayText, setDisplayText] = useState(placeholders[0]);
  const [isDeleting, setIsDeleting] = useState(false);
  const [currentPlaceholderIndex, setCurrentPlaceholderIndex] = useState(0);
  const [typingSpeed, setTypingSpeed] = useState(120);
  const [isFocused, setIsFocused] = useState(false);
  const [searchText, setSearchText] = useState('');

  useEffect(() => {
    let timeout;

    // Don't run the animation if the input is focused
    if (isFocused) {
      return () => clearTimeout(timeout);
    }

    // When the text is being deleted
    if (isDeleting) {
      if (displayText.length === 0) {
        // When fully deleted, switch to typing mode and update current placeholder
        setIsDeleting(false);
        setCurrentPlaceholderIndex(
          (prevIndex) => (prevIndex + 1) % placeholders.length
        );
        setTypingSpeed(120);
      } else {
        // Continue deleting one character at a time
        timeout = setTimeout(() => {
          setDisplayText((prevText) => prevText.slice(0, -1));
        }, typingSpeed / 2);
      }
    }
    // When the text is being typed
    else {
      const fullText = placeholders[currentPlaceholderIndex];

      if (displayText.length === fullText.length) {
        // When fully typed, pause for 3 seconds before starting to delete
        timeout = setTimeout(() => {
          setIsDeleting(true);
        }, 3000);
      } else {
        // Continue typing one character at a time
        timeout = setTimeout(() => {
          setDisplayText((prevText) => fullText.slice(0, prevText.length + 1));
        }, typingSpeed / 2);
      }
    }

    return () => clearTimeout(timeout);
  }, [
    displayText,
    isDeleting,
    currentPlaceholderIndex,
    placeholders,
    typingSpeed,
    isFocused,
  ]);

  return (
    <div className="container">
      <div className="logo">
        <div className="logo-circles">
          <div className="circle circle-orange"></div>
          <div className="circle circle-green"></div>
          <div className="circle circle-blue"></div>
        </div>
        Is it Cinema?
      </div>

      <div className="search-container">
        <input
          type="text"
          className="search-box"
          placeholder=""
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={(e) => {
            if (e.target.value === '') {
              setIsFocused(false);
            }
          }}
        />
        {!isFocused && (
          <div className="placeholder-animation-container">
            <div className="placeholder-text typing">
              {displayText}
              <span className="cursor"></span>
            </div>
          </div>
        )}
      </div>

      <div className="buttons">
        <button
          className="button summary-button"
          onClick={() => {
            if (searchText.trim()) {
              navigate('/movie-info', { state: { searchQuery: searchText } });
            }
          }}
        >
          Movie Summary
        </button>

        <button
          className="button roast-button"
          onClick={() => {
            if (searchText.trim()) {
              navigate('/roast', { state: { searchQuery: searchText } });
            }
          }}
        >
          Roast my letterboxd
        </button>
      </div>
    </div>
  );
};

export default Landing;
