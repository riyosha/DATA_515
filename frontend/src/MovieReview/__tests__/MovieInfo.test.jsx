import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import MovieInfo from '../MovieInfo';

describe('MovieInfo Component', () => {
  const defaultProps = {
    name: 'The Godfather',
    director: 'Francis Ford Coppola',
    year: '1972',
    genres: ['Crime', 'Drama'],
    synopsis: 'The aging patriarch of an organized crime dynasty transfers control to his reluctant son.',
    review: 'A masterpiece of cinema that redefined the gangster genre.'
  };

  it('renders the movie name and year correctly', () => {
    render(<MovieInfo {...defaultProps} />);
    
    expect(screen.getByText(/The Godfather/i)).toBeInTheDocument();
    expect(screen.getByText(/\(1972\)/i)).toBeInTheDocument();
  });

  it('renders the director information', () => {
    render(<MovieInfo {...defaultProps} />);
    
    expect(screen.getByText(/Directed by Francis Ford Coppola/i)).toBeInTheDocument();
  });

  it('renders genre list correctly when passed as an array', () => {
    render(<MovieInfo {...defaultProps} />);
    
    expect(screen.getByText(/Crime, Drama/i)).toBeInTheDocument();
  });

  it('renders genre correctly when passed as a string', () => {
    const propsWithStringGenre = {
      ...defaultProps,
      genres: 'Science Fiction'
    };
    
    render(<MovieInfo {...propsWithStringGenre} />);
    
    expect(screen.getByText(/Science Fiction/i)).toBeInTheDocument();
  });

  it('renders synopsis with correct heading', () => {
    render(<MovieInfo {...defaultProps} />);
    
    expect(screen.getByText('Synopsis')).toBeInTheDocument();
    expect(screen.getByText(defaultProps.synopsis)).toBeInTheDocument();
  });

  it('renders review with correct heading', () => {
    render(<MovieInfo {...defaultProps} />);
    
    expect(screen.getByText('Letterboxd Take')).toBeInTheDocument();
    expect(screen.getByText(defaultProps.review)).toBeInTheDocument();
  });

  it('renders without crashing when all required props are provided', () => {
    expect(() => render(<MovieInfo {...defaultProps} />)).not.toThrow();
  });
});