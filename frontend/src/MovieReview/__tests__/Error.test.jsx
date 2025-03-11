import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Error from '../Error';

describe('Error Component', () => {
  it('renders the error message', () => {
    render(<Error />);

    expect(
      screen.getByText(/This page got a 0% on Rotten Tomatoes/i)
    ).toBeInTheDocument();
    expect(
      screen.getByText(/And trust us, that's not good. Try again later!/i)
    ).toBeInTheDocument();
  });
});
