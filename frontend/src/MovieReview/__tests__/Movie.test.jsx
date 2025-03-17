import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Movie from '../Movie';
import MovieInfo from '../MovieInfo';
// import Video from '../Video';
import Error from '../Error';

// Mock the component dependencies
vi.mock('../MovieInfo', () => {
  return {
    default: vi.fn(() => <div data-testid="movie">Movie Component</div>),
  };
});

vi.mock('../Video', () => {
  return {
    default: vi.fn(({ videoPath }) => (
      <div data-testid="video">{videoPath}</div>
    )),
  };
});

vi.mock('../Error', () => {
  return {
    default: vi.fn(() => <div data-testid="error">Error Component</div>),
  };
});

describe('Movie Component', () => {
  // Mock fetch before each test
  beforeEach(() => {
    global.fetch = vi.fn();
    console.error = vi.fn();
  });

  // Clean up after each test
  afterEach(() => {
    vi.clearAllMocks();
  });

  it('displays loading video while fetching data', async () => {
    // Mock a slow response
    global.fetch.mockImplementationOnce(
      () =>
        new Promise((resolve) =>
          setTimeout(
            () =>
              resolve({
                ok: true,
                json: () =>
                  Promise.resolve({
                    title: 'Test Movie',
                    director: 'Test Director',
                    release_year: '2023',
                    genres: ['Action', 'Drama'],
                    poster_url: 'test-image.jpg',
                    overview: 'Test synopsis',
                    critic_review: 'Test review',
                  }),
              }),
            100
          )
        )
    );

    render(<Movie />);

    // Should show the loading video initially
    expect(screen.getByTestId('video')).toBeInTheDocument();
    expect(screen.getByText('/videos/go-to-the-lobby.mp4')).toBeInTheDocument();

    // Wait for loading to complete and verify it's gone
    await waitFor(
      () => {
        expect(screen.queryByTestId('video')).not.toBeInTheDocument();
      },
      { timeout: 2000 }
    );
  });

  it('renders MovieInfo with correct data after successful fetch', async () => {
    // Mock successful API response
    const mockMovieData = {
      title: 'Test Movie',
      director: 'Test Director',
      release_year: '2023',
      genres: ['Action', 'Drama'],
      poster_url: 'test-image.jpg',
      overview: 'Test synopsis',
      critic_review: 'Test review',
    };

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockMovieData),
    });

    render(<Movie />);

    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.getByTestId('movie')).toBeInTheDocument();
    });

    // Check that MovieInfo was called with the correctly processed data
    expect(MovieInfo).toHaveBeenCalledWith(
      {
        name: 'Test Movie',
        director: 'Test Director',
        year: '2023',
        genres: ['Action', 'Drama'],
        backgroundImage: 'test-image.jpg',
        synopsis: 'Test synopsis',
        review: 'Test review',
      },
      undefined
    );
  });

  it('shows error component when fetch fails', async () => {
    // Mock failed API response
    global.fetch.mockRejectedValueOnce(new Error('Network error'));

    render(<Movie />);

    // Wait for error component to appear
    await waitFor(() => {
      expect(screen.getByTestId('error')).toBeInTheDocument();
    });

    // Verify that error was logged to console
    expect(console.error).toHaveBeenCalled();
  });

  it('shows error component when API returns non-OK response', async () => {
    // Mock API error response
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 404,
    });

    render(<Movie />);

    // Wait for error component to appear
    await waitFor(() => {
      expect(screen.getByTestId('error')).toBeInTheDocument();
    });
  });

  it('handles missing data in API response', async () => {
    // Mock API response with minimal data
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () =>
        Promise.resolve({
          title: 'Minimal Movie',
          director: 'Some Director',
          release_year: '2022',
          // Missing genres, poster_url, etc.
        }),
    });

    render(<Movie />);

    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.getByTestId('movie')).toBeInTheDocument();
    });

    // Check that MovieInfo handles missing data gracefully
    expect(MovieInfo).toHaveBeenCalledWith(
      expect.objectContaining({
        name: 'Minimal Movie',
        director: 'Some Director',
        year: '2022',
        genres: [], // Should default to empty array
        review: 'No review available', // Should use default message
        backgroundImage: undefined, // Should default to undefined
        synopsis: undefined, // Should default to undefined
      }),
      undefined
    );
  });
});
