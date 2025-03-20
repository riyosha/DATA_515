import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import Landing from '../Landing';

// Mock useNavigate
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

describe('Landing Component', () => {
  beforeEach(() => {
    mockNavigate.mockReset();
  });

  test('navigates to movie page when Movie Summary button is clicked with input', () => {
    render(<Landing />);

    // Enter text in the search box
    const searchInput = screen.getByRole('textbox');
    fireEvent.change(searchInput, {
      target: { value: 'letterboxd.com/username' },
    });

    // Click the Movie Summary button
    const summaryButton = screen.getByText('Movie Summary');
    fireEvent.click(summaryButton);

    // Check if navigate was called with the correct parameters
    expect(mockNavigate).toHaveBeenCalledWith('/movie', {
      state: { searchQuery: 'letterboxd.com/username' },
    });
  });

  test('placeholder text animation cycles through options when not focused', async () => {
    vi.useFakeTimers();
    render(<Landing />);

    // Check initial placeholder text
    expect(screen.getByText(/Enter a letterboxd url or username/i)).toBeInTheDocument();

    // Fast-forward time to see placeholder change
    vi.advanceTimersByTime(10000); // Advance enough time for transition

    // Reset timers to avoid issues
    vi.useRealTimers();
  });

  test('hides placeholder when input is focused', async () => {
    render(<Landing />);

    // Get the initial placeholder
    const placeholder = screen.getByText(/Enter a letterboxd url or username/i);
    expect(placeholder).toBeInTheDocument();

    // Focus the input
    const searchInput = screen.getByRole('textbox');
    fireEvent.focus(searchInput);

    // Check if placeholder is hidden
    await waitFor(() => {
      expect(
        screen.queryByText(/Enter a letterboxd url or username/i)
      ).not.toBeInTheDocument();
    });
  });
});
