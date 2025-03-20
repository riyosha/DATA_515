import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import PropTypes from 'prop-types';

const AspectGraph = ({ data }) => {
  // Ensure data is an array, even if null or undefined is passed
  const safeData = Array.isArray(data) ? data : [];

  // Transform the array data into the format required by Recharts
  const transformData = () => {
    return safeData.map(([aspect, positive, negative]) => ({
      aspect,
      value1: positive,
      value2: negative,
    }));
  };

  const chartData = transformData();

  // Custom tooltip formatter to add % sign
  const customTooltipFormatter = (value) => {
    return `${value}%`;
  };

  // Explicit styling to replace Tailwind classes
  const styles = {
    container: {
      width: '100%',
      height: '400px',
      display: 'flex',
      flexDirection: 'column',
      marginTop: '30px',
      marginBottom: '30px',
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      padding: '20px',
      borderRadius: '8px',
    },
    title: {
      fontSize: '1.25rem',
      fontWeight: 'bold',
      textAlign: 'center',
      marginBottom: '1rem',
    },
    chartContainer: {
      flexGrow: 1,
    },
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Aspect Comparison</h2>
      <div style={styles.chartContainer}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            margin={{
              top: 20,
              right: 30,
              left: 20,
              bottom: 30,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#555" />
            <XAxis dataKey="aspect" stroke="#fff" />
            <YAxis
              domain={[0, 100]}
              stroke="#fff"
              tickFormatter={customTooltipFormatter}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#333',
                color: '#fff',
                border: 'none',
              }}
              formatter={(value, name) => {
                // Return the value with % sign and preserve the name for the tooltip
                return [`${value}%`, name === 'value1' ? 'Like' : 'Dislike'];
              }}
            />
            <Legend wrapperStyle={{ color: '#fff' }} />
            <Bar dataKey="value1" fill="#00e054" name="Like" />
            <Bar dataKey="value2" fill="#ff8000" name="Dislike" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

// Add prop types validation
AspectGraph.propTypes = {
  data: PropTypes.array,
};

// Add default props
AspectGraph.defaultProps = {
  data: [],
};

export default AspectGraph;
