import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import VibeCheck from '../VibeCheck';

// Mock fetch globally
global.fetch = vi.fn();

// Helper to mock fetch responses
function mockFetchResponse(data, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: () => Promise.resolve(data),
  };
}

describe('VibeCheck Component', () => {
  const filmUrl = 'https://letterboxd.com/film/pulp-fiction/';

  beforeEach(() => {
    // Reset mocks before each test
    vi.clearAllMocks();
    global.fetch.mockReset();
  });

  it('renders the component with title and form', () => {
    render(<VibeCheck filmUrl={filmUrl} />);

    // Check for title
    expect(screen.getByText('Vibe check this movie')).toBeInTheDocument();

    // Check for form elements
    expect(
      screen.getByPlaceholderText('Enter letterboxd username')
    ).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Submit' })).toBeInTheDocument();
  });

  it('shows error when submitting empty username', async () => {
    render(<VibeCheck filmUrl={filmUrl} />);

    // Submit form with empty input
    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));

    // Check for error message
    expect(screen.getByText('Please enter a username')).toBeInTheDocument();

    // Verify that fetch was not called
    expect(fetch).not.toHaveBeenCalled();
  });

  it('makes API call with correct data when form is submitted', async () => {
    // Mock successful API response
    global.fetch.mockResolvedValueOnce(
      mockFetchResponse({ taste: 'Great taste match!' })
    );

    // Render component
    render(<VibeCheck filmUrl={filmUrl} />);

    // Fill form and submit
    const testUsername = 'moviefan123';
    fireEvent.change(screen.getByPlaceholderText('Enter letterboxd username'), {
      target: { value: testUsername },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));

    // Check that form shows loading state
    expect(screen.getByText('Checking...')).toBeInTheDocument();
    expect(screen.getByText('Checking the vibes...')).toBeInTheDocument();

    // Verify API call was made with correct parameters
    expect(fetch).toHaveBeenCalledWith('/api/taste', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        film_url: filmUrl,
        username: testUsername,
      }),
    });

    // Wait for results to show
    await waitFor(() => {
      expect(screen.getByText('Results for moviefan123')).toBeInTheDocument();
      expect(screen.getByText('Great taste match!')).toBeInTheDocument();
    });
  });

  it('shows error message when API call fails', async () => {
    // Mock failed API response
    global.fetch.mockRejectedValueOnce(new Error('Network error'));

    // Render component
    render(<VibeCheck filmUrl={filmUrl} />);

    // Fill form and submit
    fireEvent.change(screen.getByPlaceholderText('Enter letterboxd username'), {
      target: { value: 'moviefan123' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));

    // Wait for error message
    await waitFor(() => {
      expect(
        screen.getByText('Failed to get vibe check. Please try again.')
      ).toBeInTheDocument();
    });
  });

  it('shows message when response has no taste data', async () => {
    // Mock API response with no taste data
    global.fetch.mockResolvedValueOnce(
      mockFetchResponse({ otherData: 'some data but no taste' })
    );

    // Render component
    render(<VibeCheck filmUrl={filmUrl} />);

    // Fill form and submit
    fireEvent.change(screen.getByPlaceholderText('Enter letterboxd username'), {
      target: { value: 'moviefan123' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));

    // Wait for no data message
    await waitFor(() => {
      expect(
        screen.getByText('No vibe match information available.')
      ).toBeInTheDocument();
    });
  });

  it('disables input and button during loading state', async () => {
    // Mock slow API response to test loading state
    global.fetch.mockImplementationOnce(() => {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(mockFetchResponse({ taste: 'Response after delay' }));
        }, 100);
      });
    });

    // Render component
    render(<VibeCheck filmUrl={filmUrl} />);

    // Get form elements
    const input = screen.getByPlaceholderText('Enter letterboxd username');
    const button = screen.getByRole('button', { name: 'Submit' });

    // Fill form and submit
    fireEvent.change(input, { target: { value: 'moviefan123' } });
    fireEvent.click(button);

    // Check that input and button are disabled during loading
    expect(input).toBeDisabled();
    expect(button).toBeDisabled();
    expect(button).toHaveTextContent('Checking...');

    // Wait for loading to complete
    await waitFor(() => {
      expect(input).not.toBeDisabled();
      expect(button).not.toBeDisabled();
      expect(button).toHaveTextContent('Submit');
    });
  });

  it('trims whitespace from entered username', async () => {
    // Mock successful API response
    global.fetch.mockResolvedValueOnce(
      mockFetchResponse({ taste: 'Great taste match!' })
    );

    // Render component
    render(<VibeCheck filmUrl={filmUrl} />);

    // Fill form with username that has whitespace
    const untrimmedUsername = '  moviefan123  ';
    fireEvent.change(screen.getByPlaceholderText('Enter letterboxd username'), {
      target: { value: untrimmedUsername },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));

    // Verify API call was made with trimmed username
    expect(fetch).toHaveBeenCalledWith(
      '/api/taste',
      expect.objectContaining({
        body: JSON.stringify({
          film_url: filmUrl,
          username: 'moviefan123', // trimmed value
        }),
      })
    );
  });

  it('clears previous results when submitting form again', async () => {
    // Mock two successful API responses
    global.fetch
      .mockResolvedValueOnce(mockFetchResponse({ taste: 'First response' }))
      .mockResolvedValueOnce(mockFetchResponse({ taste: 'Second response' }));

    // Render component
    render(<VibeCheck filmUrl={filmUrl} />);

    // Fill form and submit the first time
    fireEvent.change(screen.getByPlaceholderText('Enter letterboxd username'), {
      target: { value: 'user1' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));

    // Wait for first result
    await waitFor(() => {
      expect(screen.getByText('First response')).toBeInTheDocument();
    });

    // Fill form and submit again
    fireEvent.change(screen.getByPlaceholderText('Enter letterboxd username'), {
      target: { value: 'user2' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));

    // During loading, the previous result should be cleared
    expect(screen.queryByText('First response')).not.toBeInTheDocument();

    // Wait for second result
    await waitFor(() => {
      expect(screen.getByText('Second response')).toBeInTheDocument();
    });
  });
});
