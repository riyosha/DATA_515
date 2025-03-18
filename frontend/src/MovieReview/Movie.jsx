import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import MovieInfo from './MovieInfo';
import Video from './Video';
import Error from './Error';
import AspectGraph from './AspectGraph';
import './Movie.css';

const Movie = () => {
  const [movieData, setMovieData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const location = useLocation();

  useEffect(() => {
    // Function to fetch data
    const fetchMovieData = async () => {
      try {
        // Get the searchQuery from the location state (passed from the previous page)
        const searchQuery = location.state?.searchQuery;

        const response = await fetch('/api/movie_details', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ film_url: searchQuery }),
        });

        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();

        // Process API data
        const processedData = {
          name: data.movie_details.movie_name,
          director: data.movie_details.director,
          year: data.movie_details.year,
          genres: data.movie_details.genres
            ? data.movie_details.genres
                .split(',')
                .map((genre) => genre.trim())
                .filter((genre) => genre)
                .slice(0, 5)
            : [],
          backgroundImage: data.movie_details.backdrop_image_url,
          synopsis: data.movie_details.synopsis,
          // Add other fields as needed
          review: data.summary || 'No review available',
          // aspects: data.aspects || null,
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
  }, [location.state]);

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
          console.log(movieData);
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
