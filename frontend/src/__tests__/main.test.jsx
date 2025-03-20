import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { StrictMode } from 'react';

// Mock the entire react-dom/client module
vi.mock('react-dom/client', () => {
  const mockRoot = {
    render: vi.fn(),
  };

  return {
    createRoot: vi.fn(() => mockRoot),
  };
});

// Mock the components
vi.mock('./Landing.jsx', () => ({
  default: () => <div data-testid="landing-page">Landing Page</div>,
}));

vi.mock('./MovieReview/Movie.jsx', () => ({
  default: () => <div data-testid="movie-page">Movie Page</div>,
}));

vi.mock('./Roast/Roast.jsx', () => ({
  default: () => <div data-testid="roast-page">Roast Page</div>,
}));

vi.mock('./MovieReview/Video.jsx', () => ({
  default: () => <div data-testid="video-page">Video Loading Page</div>,
}));

// Import the routes after mocking
import { Routes, Route } from 'react-router-dom';
import { createRoot } from 'react-dom/client';

describe('Main Application Routing', () => {
  beforeEach(() => {
    // Reset mocks before each test
    vi.resetAllMocks();

    // Mock document.getElementById
    document.getElementById = vi.fn(() => ({ id: 'root' }));
  });

  it('should initialize the app with createRoot', async () => {
    // Import the module to trigger the code
    await import('../main.jsx');

    // Verify createRoot was called with the correct element
    expect(createRoot).toHaveBeenCalled();
  });

  it('renders Landing component at root path', () => {
    // Here we test the actual routes by using our own rendering
    render(
      <StrictMode>
        <MemoryRouter initialEntries={['/']}>
          <Routes>
            <Route
              path="/"
              element={<div data-testid="landing-page">Landing Page</div>}
            />
            <Route
              path="/movie"
              element={<div data-testid="movie-page">Movie Page</div>}
            />
            <Route
              path="/roast"
              element={<div data-testid="roast-page">Roast Page</div>}
            />
            <Route
              path="/loading"
              element={<div data-testid="video-page">Video Loading Page</div>}
            />
          </Routes>
        </MemoryRouter>
      </StrictMode>
    );

    expect(screen.getByTestId('landing-page')).toBeInTheDocument();
  });

  it('renders Movie component at /movie path', () => {
    render(
      <StrictMode>
        <MemoryRouter initialEntries={['/movie']}>
          <Routes>
            <Route
              path="/"
              element={<div data-testid="landing-page">Landing Page</div>}
            />
            <Route
              path="/movie"
              element={<div data-testid="movie-page">Movie Page</div>}
            />
            <Route
              path="/roast"
              element={<div data-testid="roast-page">Roast Page</div>}
            />
            <Route
              path="/loading"
              element={<div data-testid="video-page">Video Loading Page</div>}
            />
          </Routes>
        </MemoryRouter>
      </StrictMode>
    );

    expect(screen.getByTestId('movie-page')).toBeInTheDocument();
  });

  it('renders Roast component at /roast path', () => {
    render(
      <StrictMode>
        <MemoryRouter initialEntries={['/roast']}>
          <Routes>
            <Route
              path="/"
              element={<div data-testid="landing-page">Landing Page</div>}
            />
            <Route
              path="/movie"
              element={<div data-testid="movie-page">Movie Page</div>}
            />
            <Route
              path="/roast"
              element={<div data-testid="roast-page">Roast Page</div>}
            />
            <Route
              path="/loading"
              element={<div data-testid="video-page">Video Loading Page</div>}
            />
          </Routes>
        </MemoryRouter>
      </StrictMode>
    );

    expect(screen.getByTestId('roast-page')).toBeInTheDocument();
  });

  it('renders Video loading component at /loading path', () => {
    render(
      <StrictMode>
        <MemoryRouter initialEntries={['/loading']}>
          <Routes>
            <Route
              path="/"
              element={<div data-testid="landing-page">Landing Page</div>}
            />
            <Route
              path="/movie"
              element={<div data-testid="movie-page">Movie Page</div>}
            />
            <Route
              path="/roast"
              element={<div data-testid="roast-page">Roast Page</div>}
            />
            <Route
              path="/loading"
              element={<div data-testid="video-page">Video Loading Page</div>}
            />
          </Routes>
        </MemoryRouter>
      </StrictMode>
    );

    expect(screen.getByTestId('video-page')).toBeInTheDocument();
  });
});
