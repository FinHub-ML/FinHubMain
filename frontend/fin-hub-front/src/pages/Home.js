import React, { useState } from 'react';
import { PieChart } from '@mui/x-charts/PieChart';
import { Container, TextField, Button } from '@mui/material';
import HeadImage from '../images/p1.png';
import FloatingKeywords from './FloatingKeywords';

const Home = () => {
  const [positiveCount, setPositiveCount] = useState(2);
  const [negativeCount, setNegativeCount] = useState(2);
  const [neutralCount, setNeutralCount] = useState(3);
  const [keywords, setKeywords] = useState([
    'Oil price plummet',
    'TESLA new car',
    'iPhone 16',
  ]);

  const handleInputChange = (event, setter) => {
    const value = parseInt(event.target.value, 10);
    setter(value >= 0 ? value : 0);
  };

  const pieChartData = [
    { id: 0, value: positiveCount, label: 'Positive' },
    { id: 1, value: negativeCount, label: 'Negative' },
    { id: 2, value: neutralCount, label: 'Neutral' },
  ];

  const totalCount = positiveCount + negativeCount + neutralCount;
  let sentiment = 'neutral';
  if (positiveCount > negativeCount && positiveCount > neutralCount) {
    sentiment = 'positive';
  } else if (negativeCount > positiveCount && negativeCount > neutralCount) {
    sentiment = 'negative';
  }

  const gradientColors = {
    positive: 'linear-gradient(to top, #008566, rgba(0, 133, 102, 0))',
    negative: 'linear-gradient(to top, #E50808, rgba(229, 8, 8, 0))',
    neutral: 'linear-gradient(to top, #006CB8, rgba(0, 108, 184, 0))',
  };

  const handleKeywordsChange = (event) => {
    const newKeywords = event.target.value.split(',').map((keyword) => keyword.trim());
    setKeywords(newKeywords);
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        // transition: 'all 2s ease',
      }}
    >
      <img
        src={HeadImage}
        alt="HeadImage"
        style={{
          width: '100%',
          maxHeight: '95vh',
          objectFit: 'cover',
          objectPosition: 'center',
        }}
      />
      <h1
        style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          color: 'white',
          fontSize: '6rem',
          textAlign: 'center',
          mixBlendMode: 'difference',
          textShadow: '2px 2px 4px rgba(0, 0, 0, 0.5)',
        }}
      >
        Market Sentiment Today
      </h1>

      <Container style={{ marginTop: 100 }}>
        <div style={{ textAlign: 'center' }}>
          <TextField
            label="Positive Count"
            type="number"
            value={positiveCount}
            onChange={(event) => handleInputChange(event, setPositiveCount)}
            InputLabelProps={{
              style: {
                fontSize: '1.2rem',
                fontWeight: 'bold',
                color: '#000',
              },
            }}
          />
          <TextField
            label="Negative Count"
            type="number"
            value={negativeCount}
            onChange={(event) => handleInputChange(event, setNegativeCount)}
            InputLabelProps={{
              style: {
                fontSize: '1.2rem',
                fontWeight: 'bold',
                color: '#000',
              },
            }}
          />
          <TextField
            label="Neutral Count"
            type="number"
            value={neutralCount}
            onChange={(event) => handleInputChange(event, setNeutralCount)}
            InputLabelProps={{
              style: {
                fontSize: '1.2rem',
                fontWeight: 'bold',
                color: '#000',
              },
            }}
          />
        </div>
        <div style={{ position: 'relative', height: 400, width: '100%', paddingTop: 50, paddingBottom: 50 }}>
          <PieChart
            colors={[' #008566', ' #E50808', '#006CB8']}
            series={[
              {
                data: pieChartData,
                innerRadius: 0,
                outerRadius: 150,
                cornerRadius: 5,
              },
            ]}
          />
          <FloatingKeywords keywords={keywords} />

        </div>
        <div style={{ textAlign: 'center', marginTop: 20 }}>
          <TextField
            label="Keywords (comma-separated)"
            value={keywords.join(', ')}
            onChange={handleKeywordsChange}
            fullWidth
            InputLabelProps={{
              style: {
                fontSize: '1.2rem',
                fontWeight: 'bold',
                color: '#000',
              },
            }}
          />
        </div>
      </Container>
    </div>
  );
};

export default Home;