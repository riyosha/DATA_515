import { useState, useEffect } from 'react';
import MovieInfo from './MovieInfo';
import Video from './Video';
import Error from './Error';

const Movie = () => {
  const [movieData, setMovieData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Function to fetch data
    const fetchMovieData = async () => {
      try {
        let processedData;

        /*
        // MOCK DATA FOR LOCAL TESTING - Uncomment this block and comment the API code below to test locally and vice versa
        const startTime = Date.now();
        const minimumLoadingTime = 1000;
        
        processedData = {
          name: "Moonfall",
          director: "Roland Emmerich",
          year: "2022",
          genres: ["Sci-Fi", "Adventure", "Action"],
          backgroundImage: "https://m.media-amazon.com/images/M/MV5BZjk0OWZiN2ItNmQ2YS00NTJmLTg0MjItNzM4NzBkMWM1ZTRlXkEyXkFqcGdeQXVyMjMxOTE0ODA@._V1_.jpg",
          synopsis: "A space crew travels to the moon after it's struck by an asteroid and is sent on a collision course with Earth.",
          review: "This is the worst movie ever made by mankind. It's so bad that it's good. You have to see it to believe it."
        };
        
        // Simulate API call time
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // For mock data only: ensure minimum loading time
        const elapsedTime = Date.now() - startTime;
        if (elapsedTime < minimumLoadingTime) {
          const remainingTime = minimumLoadingTime - elapsedTime;
          await new Promise(resolve => setTimeout(resolve, remainingTime));
        }

        */

        const response = await fetch('https://your-api-endpoint.com/movie/123');
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        const data = await response.json();

        // Process API data into the format your component expects
        processedData = {
          name: data.title,
          director: data.director,
          year: data.release_year,
          genres: data.genres || [],
          backgroundImage: data.poster_url,
          synopsis: data.overview,
          review: data.critic_review || 'No review available',
        };

        // Update state with fetched data
        setMovieData(processedData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching movie data:', err);
        setError('Failed to fetch movie data');
        setLoading(false);
      }
    };

    fetchMovieData();
  }, []);

  if (loading) {
    return <Video videoPath="/videos/go-to-the-lobby.mp4" />;
  }

  if (error) {
    return <Error />;
  }

  return (
    <div
      style={{
        position: 'relative',
        minHeight: '100vh',
        backgroundColor: '#000',
        color: '#fff',
      }}
    >
      {/* Background Image with dark overlay */}
      <div
        style={{
          position: 'fixed',
          inset: 0,
          backgroundImage: `url(${movieData.backgroundImage})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          zIndex: 1,
        }}
      >
        <div
          style={{
            position: 'absolute',
            inset: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
          }}
        ></div>
      </div>

      {/* Content container */}
      <div
        style={{
          position: 'relative',
          zIndex: 2,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '100vh',
          padding: '0 2rem',
        }}
      >
        <div
          style={{
            maxWidth: '72rem',
            width: '100%',
          }}
        >
          <MovieInfo {...movieData} />
        </div>
      </div>
    </div>
  );
};

export default Movie;
