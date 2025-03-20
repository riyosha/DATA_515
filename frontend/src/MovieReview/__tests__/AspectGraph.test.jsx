import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom';
import AspectGraph from '../AspectGraph';

// Use eslint-disable to avoid prop-types warnings in test mocks
/* eslint-disable react/prop-types */
vi.mock('recharts', () => {
  const OriginalModule = vi.importActual('recharts');
  return {
    ...OriginalModule,
    ResponsiveContainer: function MockResponsiveContainer({ children }) {
      return <div data-testid="responsive-container">{children}</div>;
    },
    BarChart: function MockBarChart({ children, data }) {
      return (
        <div data-testid="bar-chart" data-chartdata={JSON.stringify(data)}>
          {children}
        </div>
      );
    },
    Bar: function MockBar({ dataKey, fill, name }) {
      return (
        <div
          data-testid={`bar-${dataKey}`}
          data-fill={fill}
          data-name={name}
        ></div>
      );
    },
    XAxis: function MockXAxis({ dataKey }) {
      return <div data-testid="x-axis" data-key={dataKey}></div>;
    },
    YAxis: function MockYAxis({ domain, tickFormatter }) {
      return (
        <div
          data-testid="y-axis"
          data-domain={JSON.stringify(domain)}
          data-has-formatter={Boolean(tickFormatter).toString()}
        ></div>
      );
    },
    CartesianGrid: function MockCartesianGrid() {
      return <div data-testid="cartesian-grid"></div>;
    },
    Tooltip: function MockTooltip({ formatter }) {
      // Test the formatter function with a sample value
      let formattedValue = null;
      let formattedName = null;

      if (formatter) {
        const result = formatter(75, 'value1');
        formattedValue = result[0];
        formattedName = result[1];
      }

      return (
        <div
          data-testid="tooltip"
          data-has-formatter={Boolean(formatter).toString()}
          data-formatted-value={formattedValue}
          data-formatted-name={formattedName}
        ></div>
      );
    },
    Legend: function MockLegend() {
      return <div data-testid="legend"></div>;
    },
  };
});
/* eslint-enable react/prop-types */

describe('AspectGraph Component', () => {
  // Sample test data
  const testData = [
    ['Story', 85, 90],
    ['Acting', 92, 88],
    ['Visuals', 78, 65],
    ['Soundtrack', 88, 72],
  ];

  it('renders without crashing', () => {
    const { getByTestId } = render(<AspectGraph data={testData} />);
    expect(getByTestId('responsive-container')).toBeInTheDocument();
    expect(getByTestId('bar-chart')).toBeInTheDocument();
  });

  it('transforms data correctly', () => {
    const { getByTestId } = render(<AspectGraph data={testData} />);

    // Get transformed chart data from the BarChart component
    const chartDataAttr =
      getByTestId('bar-chart').getAttribute('data-chartdata');
    const chartData = JSON.parse(chartDataAttr);

    // Check if the data was transformed correctly
    expect(chartData).toHaveLength(4);

    expect(chartData[0]).toEqual({ aspect: 'Story', value1: 85, value2: 90 });
    expect(chartData[1]).toEqual({ aspect: 'Acting', value1: 92, value2: 88 });
  });

  it('sets Y-axis domain to fixed range of 0-100', () => {
    const { getByTestId } = render(<AspectGraph data={testData} />);

    // Get the domain from the YAxis component
    const yAxisDomain = getByTestId('y-axis').getAttribute('data-domain');
    const domain = JSON.parse(yAxisDomain);

    // The domain should be fixed at [0, 100]
    expect(domain).toEqual([0, 100]);
  });

  it('has a Y-axis formatter to add percentage sign', () => {
    const { getByTestId } = render(<AspectGraph data={testData} />);

    // Check if the Y-axis has a formatter function
    expect(getByTestId('y-axis')).toHaveAttribute('data-has-formatter', 'true');
  });

  it('has a tooltip formatter that adds percentage sign and preserves labels', () => {
    const { getByTestId } = render(<AspectGraph data={testData} />);

    // Check if the tooltip has a formatter function
    const tooltip = getByTestId('tooltip');
    expect(tooltip).toHaveAttribute('data-has-formatter', 'true');

    // Check the formatted value has a % sign
    expect(tooltip).toHaveAttribute('data-formatted-value', '75%');

    // Check that the label is set to "Like" for value1
    expect(tooltip).toHaveAttribute('data-formatted-name', 'Like');
  });

  it('handles empty data array', () => {
    const { getByTestId } = render(<AspectGraph data={[]} />);

    // Check that the component still renders
    expect(getByTestId('responsive-container')).toBeInTheDocument();

    // Get transformed chart data - should be empty array
    const chartDataAttr =
      getByTestId('bar-chart').getAttribute('data-chartdata');
    const chartData = JSON.parse(chartDataAttr);
    expect(chartData).toHaveLength(0);

    // Domain should still be fixed at [0, 100]
    const yAxisDomain = getByTestId('y-axis').getAttribute('data-domain');
    const domain = JSON.parse(yAxisDomain);
    expect(domain).toEqual([0, 100]);
  });

  it('handles null or undefined data', () => {
    // Test with null
    const { getByTestId, rerender } = render(<AspectGraph data={null} />);

    let chartDataAttr = getByTestId('bar-chart').getAttribute('data-chartdata');
    let chartData = JSON.parse(chartDataAttr);
    expect(chartData).toHaveLength(0);

    // Test with undefined
    rerender(<AspectGraph data={undefined} />);

    chartDataAttr = getByTestId('bar-chart').getAttribute('data-chartdata');
    chartData = JSON.parse(chartDataAttr);
    expect(chartData).toHaveLength(0);
  });

  it('renders bar chart with correct bar props', () => {
    const { getByTestId } = render(<AspectGraph data={testData} />);

    // Check Like bar
    const likeBar = getByTestId('bar-value1');
    expect(likeBar).toHaveAttribute('data-fill', '#00e054');
    expect(likeBar).toHaveAttribute('data-name', 'Like');

    // Check Dislike bar
    const dislikeBar = getByTestId('bar-value2');
    expect(dislikeBar).toHaveAttribute('data-fill', '#ff8000');
    expect(dislikeBar).toHaveAttribute('data-name', 'Dislike');
  });
});
