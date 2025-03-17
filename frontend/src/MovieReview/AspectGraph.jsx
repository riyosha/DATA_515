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

const AspectGraph = ({ data }) => {
  // Ensure data is an object, even if null or undefined is passed
  const safeData = data || {};

  // Transform the data into the format required by Recharts
  const transformData = () => {
    return Object.entries(safeData).map(([aspect, values]) => ({
      aspect,
      value1: values[0],
      value2: values[1],
    }));
  };

  // Get the maximum value to set the domain of the YAxis
  const getMaxValue = () => {
    let max = 0;
    Object.values(safeData).forEach((values) => {
      values.forEach((value) => {
        if (value > max) {
          max = value;
        }
      });
    });
    // Add some padding to the max value
    return Math.ceil(max * 1.1);
  };

  const chartData = transformData();
  const maxValue = getMaxValue();

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
            <YAxis domain={[0, maxValue]} stroke="#fff" />
            <Tooltip
              contentStyle={{
                backgroundColor: '#333',
                color: '#fff',
                border: 'none',
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

export default AspectGraph;
