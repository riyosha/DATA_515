import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import Roast from '../Roast';
import Video from '../../MovieReview/Video';
import Error from '../../MovieReview/Error';

// Mock the components imported by Roast
vi.mock('../../MovieReview/Video', () => ({
  default: vi.fn(() => <div data-testid="video-component">Loading Video</div>),
}));

vi.mock('../../MovieReview/Error', () => ({
  default: vi.fn(() => <div data-testid="error-component">Error Occurred</div>),
}));

// Mock setTimeout to speed up tests
vi.mock('react', async () => {
  const actual = await vi.importActual('react');
  return {
    ...actual,
    // Override setTimeout for typewriter effect
    setTimeout: vi.fn((callback) => {
      callback(); // Execute callback immediately
      return 123; // Return a fake timer ID
    }),
  };
});

// Mock fetch API
global.fetch = vi.fn();

describe('Roast Component', () => {
  const mockLocation = {
    state: {
      searchQuery: 'testuser',
    },
  };

  const mockRoastResponse = {
    roast:
      'This is a test roast content. Your movie taste is questionable at best.',
  };

  beforeEach(() => {
    // Reset mocks between tests
    vi.clearAllMocks();

    // Mock successful API response by default
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockRoastResponse),
      })
    );
  });

  afterEach(() => {
    vi.resetAllMocks();
  });

  it('should render loading state (Video component) initially', () => {
    render(
      <MemoryRouter
        initialEntries={[{ pathname: '/roast', state: mockLocation.state }]}
      >
        <Routes>
          <Route path="/roast" element={<Roast />} />
        </Routes>
      </MemoryRouter>
    );

    expect(Video).toHaveBeenCalled();
    expect(screen.getByTestId('video-component')).toBeInTheDocument();
  });

  it('should render Error component when API request fails', async () => {
    // Mock a failed response
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: false,
        status: 500,
      })
    );

    render(
      <MemoryRouter
        initialEntries={[{ pathname: '/roast', state: mockLocation.state }]}
      >
        <Routes>
          <Route path="/roast" element={<Roast />} />
        </Routes>
      </MemoryRouter>
    );

    // Wait for the Error component to be rendered
    await waitFor(() => {
      expect(Error).toHaveBeenCalled();
    });
    expect(screen.getByTestId('error-component')).toBeInTheDocument();
  });

  it('should make API request with correct parameters', async () => {
    render(
      <MemoryRouter
        initialEntries={[{ pathname: '/roast', state: mockLocation.state }]}
      >
        <Routes>
          <Route path="/roast" element={<Roast />} />
        </Routes>
      </MemoryRouter>
    );

    // Verify the fetch call
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('/api/roast', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: 'testuser' }),
      });
    });
  });

  it('should render title with username after loading', async () => {
    render(
      <MemoryRouter
        initialEntries={[{ pathname: '/roast', state: mockLocation.state }]}
      >
        <Routes>
          <Route path="/roast" element={<Roast />} />
        </Routes>
      </MemoryRouter>
    );

    // Wait for the title to appear
    await waitFor(() => {
      expect(screen.queryByText('THE ROAST OF TESTUSER')).not.toBeNull();
    });
  });

  it('should fall back to "UNKNOWN USER" when no username is provided', async () => {
    render(
      <MemoryRouter initialEntries={[{ pathname: '/roast', state: {} }]}>
        <Routes>
          <Route path="/roast" element={<Roast />} />
        </Routes>
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.queryByText('THE ROAST OF UNKNOWN USER')).not.toBeNull();
    });
  });

  it('should handle fetch errors gracefully', async () => {
    // Mock a fetch that throws an error
    global.fetch = vi.fn(() => Promise.reject(new Error('Network error')));

    render(
      <MemoryRouter
        initialEntries={[{ pathname: '/roast', state: mockLocation.state }]}
      >
        <Routes>
          <Route path="/roast" element={<Roast />} />
        </Routes>
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(Error).toHaveBeenCalled();
    });
    expect(screen.getByTestId('error-component')).toBeInTheDocument();
  });

  it('should handle empty response data', async () => {
    // Mock an empty response
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({}),
      })
    );

    const { container } = render(
      <MemoryRouter
        initialEntries={[{ pathname: '/roast', state: mockLocation.state }]}
      >
        <Routes>
          <Route path="/roast" element={<Roast />} />
        </Routes>
      </MemoryRouter>
    );

    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByTestId('video-component')).not.toBeInTheDocument();
    });

    // Check that the component structure exists
    expect(container.querySelector('.roast-main-container')).not.toBeNull();
    expect(container.querySelector('.roast-content')).not.toBeNull();
    expect(container.querySelector('.roast-title')).not.toBeNull();
  });
});
