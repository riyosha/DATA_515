import { useState, useEffect, useRef } from 'react';
import './Video.css';

const Video = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);
  const videoRef = useRef(null);

  const loadingMessages = [
    'Getting your results...',
    'Remember to silence your phone...',
    'The show is about to begin...',
    'Finding the best seats in the house...',
    'Dimming the lights...',
    'No talking during the feature...',
    'Grab your popcorn...',
    'Previews of coming attractions...',
  ];

  useEffect(() => {
    // Rotate through messages every 3 seconds
    const messageInterval = setInterval(() => {
      setCurrentMessageIndex(
        (prevIndex) => (prevIndex + 1) % loadingMessages.length
      );
    }, 3000);

    return () => clearInterval(messageInterval);
  }, [loadingMessages.length]); // Add dependency to useEffect

  const handlePlayPause = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  return (
    <div className="video-container">
      {/* Loading message above the video */}
      <div className="loading-message-container">
        <div className="loading-message flashing">
          {loadingMessages[currentMessageIndex]}
        </div>
      </div>

      {/* Video with play button */}
      <div className="video-wrapper">
        <video
          ref={videoRef}
          className="video-player"
          src="/videos/go-to-the-lobby.mp4"
          onClick={handlePlayPause}
          loop
          data-testid="video-player"
        />

        {!isPlaying && (
          <button className="play-button" onClick={handlePlayPause}>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              width="48"
              height="48"
            >
              <path d="M8 5v14l11-7z" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
};

export default Video;
