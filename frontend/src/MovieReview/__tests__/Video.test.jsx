import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, cleanup } from '@testing-library/react';
import '@testing-library/jest-dom';
import Video from '../Video';

// Mock timers for the message rotation
vi.useFakeTimers();

describe('Video Component', () => {
  // Mock HTMLMediaElement.prototype methods
  beforeEach(() => {
    // Clear any mock calls before each test
    vi.clearAllMocks();
    // Setup element play and pause mocks
    window.HTMLMediaElement.prototype.play = vi.fn().mockResolvedValue();
    window.HTMLMediaElement.prototype.pause = vi.fn();
  });

  afterEach(() => {
    cleanup();
  });

  it('renders without crashing', () => {
    render(<Video />);
    const videoElement = screen.getByTestId('video-player');
    expect(videoElement).toBeInTheDocument();
  });

  it('displays a loading message', () => {
    render(<Video />);
    // Check if at least one of the possible loading messages is displayed
    const messages = [
      'Getting your results...',
      'Remember to silence your phone...',
      'The show is about to begin...',
      'Finding the best seats in the house...',
      'Dimming the lights...',
      'No talking during the feature...',
      'Grab your popcorn...',
      'Previews of coming attractions...',
    ];

    const messageElement = screen.getByText((content) => {
      return messages.some((message) => content.includes(message));
    });
    expect(messageElement).toBeInTheDocument();
  });

  it('uses setInterval to rotate messages', () => {
    // Mock setInterval
    const setIntervalSpy = vi.spyOn(global, 'setInterval');

    render(<Video />);

    // Check if setInterval was called with the correct timing
    expect(setIntervalSpy).toHaveBeenCalledWith(expect.any(Function), 3000);

    setIntervalSpy.mockRestore();
  });

  it('displays a play button initially', () => {
    render(<Video />);
    const playButton = screen.getByRole('button');
    expect(playButton).toBeInTheDocument();
  });

  it('plays video when play button is clicked', () => {
    render(<Video />);
    const playButton = screen.getByRole('button');
    fireEvent.click(playButton);

    // Check if play method was called
    expect(window.HTMLMediaElement.prototype.play).toHaveBeenCalledTimes(1);
  });

  it('hides play button when video is playing', async () => {
    const { rerender } = render(<Video />);
    const playButton = screen.getByRole('button');

    // Click play button to start video
    fireEvent.click(playButton);
    rerender(<Video />);

    // Play button should no longer be visible
    expect(screen.queryByRole('button')).not.toBeInTheDocument();
  });

  it('pauses video when clicked while playing', () => {
    render(<Video />);

    // First click play button to start playing
    const playButton = screen.getByRole('button');
    fireEvent.click(playButton);

    // Then click on the video to pause
    const videoElement = screen.getByTestId('video-player');
    fireEvent.click(videoElement);

    // Check if pause method was called
    expect(window.HTMLMediaElement.prototype.pause).toHaveBeenCalledTimes(1);
  });

  it('shows play button again when video is paused', () => {
    const { rerender } = render(<Video />);

    // First click play button to start playing
    const playButton = screen.getByRole('button');
    fireEvent.click(playButton);
    rerender(<Video />);

    // Then click on the video to pause
    const videoElement = screen.getByTestId('video-player');
    fireEvent.click(videoElement);
    rerender(<Video />);

    // Play button should be visible again
    const newPlayButton = screen.getByRole('button');
    expect(newPlayButton).toBeInTheDocument();
  });

  it('has video with correct source', () => {
    render(<Video />);
    const videoElement = screen.getByTestId('video-player');
    expect(videoElement).toHaveAttribute('src', '/videos/go-to-the-lobby.mp4');
  });

  it('has video with loop attribute', () => {
    render(<Video />);
    const videoElement = screen.getByTestId('video-player');
    expect(videoElement).toHaveAttribute('loop');
  });
});
