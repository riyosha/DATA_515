import PropTypes from 'prop-types';
import './MovieInfo.css';

const MovieInfo = ({ name, director, year, genres, review, synopsis }) => {
  return (
    <div className="movie-info-container">
      <header className="movie-header">
        <h1 className="movie-title">{name} <span className="movie-year">({year})</span></h1>
        <p className="movie-director">Directed by {director}</p>
        <p className="movie-genres">{Array.isArray(genres) ? genres.join(', ') : genres}</p>
      </header>

      <div className="movie-content">
        <div className="movie-synopsis-container">
          <h2 className="content-heading">Synopsis</h2>
          <p className="movie-synopsis">{synopsis}</p>
        </div>

        <div className="movie-review-container">
          <h2 className="content-heading">Letterboxd Take</h2>
          <p className="movie-review">{review}</p>
        </div>
      </div>
    </div>
  );
};

MovieInfo.propTypes = {
  name: PropTypes.string.isRequired,
  director: PropTypes.string.isRequired,
  year: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  genres: PropTypes.oneOfType([PropTypes.string, PropTypes.array]).isRequired,
  review: PropTypes.string.isRequired,
  synopsis: PropTypes.string.isRequired,
};

export default MovieInfo;