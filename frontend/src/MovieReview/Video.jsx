import PropTypes from 'prop-types';

const Video = ({ videoPath }) => {
  return (
    <div className="video-container">
      <p>Hello! Video path: {videoPath}</p>
    </div>
  );
};

Video.propTypes = {
  videoPath: PropTypes.string.isRequired,
};

export default Video;
