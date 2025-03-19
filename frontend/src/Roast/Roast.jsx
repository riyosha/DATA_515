import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import Video from '../MovieReview/Video';
import Error from '../MovieReview/Error';
import './Roast.css';

const Roast = () => {
  const [roastData, setRoastData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const location = useLocation();

  // Typewriter effect states
  const [displayText, setDisplayText] = useState('');
  const [currentTextIndex, setCurrentTextIndex] = useState(0);
  const [phase, setPhase] = useState('typing-positive'); // typing-positive, deleting, typing-negative, typing-roast
  const [typingComplete, setTypingComplete] = useState(false);

  // Phrases for the typewriter effect
  const positivePhrase =
    'Your letterboxd account movie preferences are insightful, masterful, inspiring...';
  const basePhrase = 'Your letterboxd account movie preferences are ';
  const negativePhrase =
    'Your letterboxd account movie preferences are dull, simple, cringe...';

  useEffect(() => {
    // Function to fetch data
    const fetchRoastData = async () => {
      try {
        // Get the searchQuery from the location state (passed from the previous page)
        const searchQuery = location.state?.searchQuery;

        const response = await fetch('/api/roast', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username: searchQuery }),
        });

        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();

        // Process API data
        const processedData = {
          title: `THE ROAST OF ${searchQuery?.toUpperCase() || 'UNKNOWN USER'}`,
          content: data.roast || 'No roast text was returned from the server.',
        };

        // Update state with fetched data
        setRoastData(processedData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching roast data:', err);
        setError('Failed to fetch roast data');
        setLoading(false);
      }
    };

    fetchRoastData();
  }, [location.state]);

  // Typewriter effect
  useEffect(() => {
    if (loading || error) return;

    let timeout;
    const typingSpeed = 50;
    const deletingSpeed = 30;
    const pauseDuration = 1500;

    // Handle different phases of the typewriter effect
    if (phase === 'typing-positive') {
      if (currentTextIndex < positivePhrase.length) {
        // Continue typing the positive phrase
        timeout = setTimeout(() => {
          setDisplayText(positivePhrase.substring(0, currentTextIndex + 1));
          setCurrentTextIndex((prev) => prev + 1);
        }, typingSpeed);
      } else {
        // Finished typing positive phrase, pause before deleting
        timeout = setTimeout(() => {
          setPhase('deleting');
          setCurrentTextIndex(positivePhrase.length);
        }, pauseDuration);
      }
    } else if (phase === 'deleting') {
      if (currentTextIndex > basePhrase.length) {
        // Continue deleting until we reach the base phrase
        timeout = setTimeout(() => {
          setDisplayText(positivePhrase.substring(0, currentTextIndex - 1));
          setCurrentTextIndex((prev) => prev - 1);
        }, deletingSpeed);
      } else {
        // Finished deleting, start typing negative phrase
        setPhase('typing-negative');
        setCurrentTextIndex(basePhrase.length);
      }
    } else if (phase === 'typing-negative') {
      if (currentTextIndex < negativePhrase.length) {
        // Continue typing the negative phrase
        timeout = setTimeout(() => {
          setDisplayText(negativePhrase.substring(0, currentTextIndex + 1));
          setCurrentTextIndex((prev) => prev + 1);
        }, typingSpeed);
      } else {
        // Finished typing negative phrase, pause before showing roast
        timeout = setTimeout(() => {
          setPhase('typing-roast');
          setCurrentTextIndex(0);
          setDisplayText(''); // Clear display text before typing roast
          setTypingComplete(true);
        }, pauseDuration);
      }
    } else if (phase === 'typing-roast' && roastData?.content) {
      if (currentTextIndex < roastData.content.length) {
        // Continue typing the roast content
        timeout = setTimeout(() => {
          setDisplayText((prev) => prev + roastData.content[currentTextIndex]);
          setCurrentTextIndex((prev) => prev + 1);
        }, typingSpeed);
      }
    }

    return () => clearTimeout(timeout);
  }, [
    loading,
    error,
    phase,
    currentTextIndex,
    roastData,
    positivePhrase,
    basePhrase,
    negativePhrase,
  ]);

  if (loading) {
    return <Video />;
  }

  if (error) {
    return <Error />;
  }

  return (
    <div className="roast-main-container">
      <div className="roast-content">
        <h1 className="roast-title">{roastData.title}</h1>

        {!typingComplete ? (
          <div className="roast-intro">
            <p>
              {displayText}
              <span className="cursor">|</span>
            </p>
          </div>
        ) : (
          <div className="roast-body">
            <p className="intro-line">{negativePhrase}</p>
            <p className="roast-text">
              {displayText}
              <span className="cursor">|</span>
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Roast;
