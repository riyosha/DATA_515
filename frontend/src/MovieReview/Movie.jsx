import { useState, useEffect } from 'react';
import MovieInfo from './MovieInfo';
import Video from './Video';
import Error from './Error';
import AspectGraph from './AspectGraph';
import './Movie.css';

const Movie = () => {
  const [movieData, setMovieData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Function to fetch data
    const fetchMovieData = async () => {
      try {
        let processedData;

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
          aspects: data.aspects || {},
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

  // No need for separate aspect data as it's now included in movieData

  return (
    <div className="movie-main-container">
      {/* Background Image */}
      <div className="movie-background-container">
        <div
          className="movie-background-image"
          style={{
            backgroundImage: `url(${movieData.backgroundImage})`,
          }}
        />
      </div>

      {/* Content */}
      <div className="movie-content-container">
        <div className="movie-info-wrapper">
          {/* Movie information section */}
          <MovieInfo {...movieData} />

          {/* Graph section with explicit class for spacing */}
          {movieData.aspects && Object.keys(movieData.aspects).length > 0 && (
            <div className="graph-container">
              <AspectGraph data={movieData.aspects} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Movie;
