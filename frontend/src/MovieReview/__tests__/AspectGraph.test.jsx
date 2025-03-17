import { describe, test, expect, beforeEach, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import AspectGraph from '../AspectGraph';

// Mock Recharts components
vi.mock('recharts', () => {
  const OriginalModule = vi.importActual('recharts');
  return {
    ...OriginalModule,
    ResponsiveContainer: ({ children }) => (
      <div data-testid="responsive-container">{children}</div>
    ),
    BarChart: vi.fn(({ children, data }) => (
      <div data-testid="bar-chart" data-chart-data={JSON.stringify(data)}>
        {children}
      </div>
    )),
    Bar: vi.fn(({ dataKey, fill, name }) => (
      <div
        data-testid={`bar-${dataKey}`}
        data-fill={fill}
        data-name={name}
      ></div>
    )),
    XAxis: vi.fn(({ dataKey, stroke }) => (
      <div data-testid="x-axis" data-key={dataKey} data-stroke={stroke}></div>
    )),
    YAxis: vi.fn(({ domain, stroke }) => (
      <div
        data-testid="y-axis"
        data-domain={JSON.stringify(domain)}
        data-stroke={stroke}
      ></div>
    )),
    CartesianGrid: vi.fn(({ strokeDasharray, stroke }) => (
      <div
        data-testid="cartesian-grid"
        data-dash={strokeDasharray}
        data-stroke={stroke}
      ></div>
    )),
    Tooltip: vi.fn(({ contentStyle }) => (
      <div
        data-testid="tooltip"
        data-style={JSON.stringify(contentStyle)}
      ></div>
    )),
    Legend: vi.fn(({ wrapperStyle }) => (
      <div data-testid="legend" data-style={JSON.stringify(wrapperStyle)}></div>
    )),
  };
});

describe('AspectGraph Component', () => {
  // Sample test data
  const testData = {
    Story: [85, 90],
    Acting: [92, 88],
    Visuals: [78, 82],
    Soundtrack: [88, 85],
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  test('renders without crashing', () => {
    render(<AspectGraph data={testData} />);
    expect(screen.getByText('Aspect Comparison')).toBeInTheDocument();
  });

  test('transforms data correctly', () => {
    render(<AspectGraph data={testData} />);

    const barChart = screen.getByTestId('bar-chart');
    const chartData = JSON.parse(barChart.getAttribute('data-chart-data'));

    // Check if the data was transformed correctly
    expect(chartData).toHaveLength(4);
    expect(chartData[0]).toEqual({ aspect: 'Story', value1: 85, value2: 90 });
    expect(chartData[1]).toEqual({ aspect: 'Acting', value1: 92, value2: 88 });
    expect(chartData[2]).toEqual({ aspect: 'Visuals', value1: 78, value2: 82 });
    expect(chartData[3]).toEqual({
      aspect: 'Soundtrack',
      value1: 88,
      value2: 85,
    });
  });

  test('calculates max value correctly with padding', () => {
    render(<AspectGraph data={testData} />);

    const yAxis = screen.getByTestId('y-axis');
    const domain = JSON.parse(yAxis.getAttribute('data-domain'));

    // The max value should be 92 * 1.1 rounded up = 102
    expect(domain[1]).toBe(102);
  });

  test('renders the correct bar elements', () => {
    render(<AspectGraph data={testData} />);

    const bar1 = screen.getByTestId('bar-value1');
    const bar2 = screen.getByTestId('bar-value2');

    expect(bar1).toBeInTheDocument();
    expect(bar2).toBeInTheDocument();

    expect(bar1.getAttribute('data-fill')).toBe('#00e054');
    expect(bar1.getAttribute('data-name')).toBe('Like');

    expect(bar2.getAttribute('data-fill')).toBe('#ff8000');
    expect(bar2.getAttribute('data-name')).toBe('Dislike');
  });

  test('applies correct styling to chart elements', () => {
    render(<AspectGraph data={testData} />);

    // Check X and Y axis styling
    const xAxis = screen.getByTestId('x-axis');
    const yAxis = screen.getByTestId('y-axis');

    expect(xAxis.getAttribute('data-stroke')).toBe('#fff');
    expect(yAxis.getAttribute('data-stroke')).toBe('#fff');

    // Check tooltip styling
    const tooltip = screen.getByTestId('tooltip');
    const tooltipStyle = JSON.parse(tooltip.getAttribute('data-style'));

    expect(tooltipStyle).toEqual({
      backgroundColor: '#333',
      color: '#fff',
      border: 'none',
    });

    // Check legend styling
    const legend = screen.getByTestId('legend');
    const legendStyle = JSON.parse(legend.getAttribute('data-style'));

    expect(legendStyle).toEqual({ color: '#fff' });
  });

  test('handles empty data gracefully', () => {
    render(<AspectGraph data={{}} />);

    const barChart = screen.getByTestId('bar-chart');
    const chartData = JSON.parse(barChart.getAttribute('data-chart-data'));

    expect(chartData).toHaveLength(0);

    const yAxis = screen.getByTestId('y-axis');
    const domain = JSON.parse(yAxis.getAttribute('data-domain'));

    // With no data, max should be 0
    expect(domain[1]).toBe(0);
  });

  test('handles null or undefined data by providing default empty object', () => {
    // Testing with undefined data
    const { rerender } = render(<AspectGraph data={undefined} />);

    let barChart = screen.getByTestId('bar-chart');
    let chartData = JSON.parse(barChart.getAttribute('data-chart-data'));

    expect(chartData).toHaveLength(0);

    // Testing with null data
    rerender(<AspectGraph data={null} />);

    barChart = screen.getByTestId('bar-chart');
    chartData = JSON.parse(barChart.getAttribute('data-chart-data'));

    expect(chartData).toHaveLength(0);
  });
});
