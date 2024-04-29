import React, { useState, useEffect } from 'react';

import ThumbUpAltIcon from '@mui/icons-material/ThumbUpAlt';
import ThumbDownAltIcon from '@mui/icons-material/ThumbDownAlt';
import IndeterminateCheckBoxIcon from '@mui/icons-material/IndeterminateCheckBox';
const SentimentDisplay = ({ text }) => {
  const [sentiment, setSentiment] = useState(null);

  useEffect(() => {
    const fetchSentiment = async () => {
      try {
        const response = await fetch('http://localhost:5000/get_sentiment', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text }),
        });

        if (response.ok) {
          const sentiment = await response.json();
          setSentiment(sentiment);
        } else {
          console.error('Error:', await response.text());
          setSentiment(null);
        }
      } catch (error) {
        console.error('Error:', error);
        setSentiment(null);
      }
    };

    fetchSentiment();
  }, [text]);

  return sentiment === 2 ? (
    <IndeterminateCheckBoxIcon />
  ) : sentiment === 1 ? (
    <ThumbUpAltIcon />
  ) : sentiment === 0 ? (
    <ThumbDownAltIcon />
  ) : null;
};

export default SentimentDisplay;