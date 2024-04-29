import React, { useState } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  CardHeader,
  CircularProgress,
} from '@mui/material';

const categoryColors = {
  LOC: { background: '#c8e6c9', text: '#388e3c', darkBackground: '#4caf50' },
  ORG: { background: '#ffcdd2', text: '#c62828', darkBackground: '#d32f2f' },
  PER: { background: '#e1bee7', text: '#7b1fa2', darkBackground: '#9c27b0' },
  MISC: { background: '#bbdefb', text: '#1976d2', darkBackground: '#2196f3' },
};

const sentimentColors = {
  2: '#90caf9', // Blue
  1: '#a5d6a7', // Green
  0: '#ef9a9a', // Red
};

function NewsList() {
  const [newsList, setNewsList] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchNews = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/news');
      if (!response.ok) {
        throw new Error('Failed to fetch news data');
      }
      const data = await response.json();
      setNewsList(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTitleClick = (url) => {
    window.open(url, '_blank');
  };

  return (
    <Box sx={{ maxWidth: 800, margin: '0 auto', padding: 2 }}>
      <Typography variant="h4" gutterBottom>
        News List
      </Typography>
      <Box display="flex" justifyContent="center" mb={2}>
        <Button
          variant="contained"
          color="primary"
          onClick={fetchNews}
          disabled={isLoading}
        >
          {isLoading ? <CircularProgress size={24} /> : 'Fetch News'}
        </Button>
      </Box>
      {error && (
        <Typography variant="body1" color="error" gutterBottom>
          Error: {error}
        </Typography>
      )}
      {newsList.map((news, index) => (
        <Card key={index} sx={{ marginBottom: 2 }}>
          <CardHeader
            title={
              <Typography
                variant="h6"
                sx={{ cursor: 'pointer' }}
                onClick={() => handleTitleClick(news.url)}
              >
                {news.title}
              </Typography>
            }
          />
          <CardContent>
            <Box
              sx={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: 1,
                alignItems: 'center',
              }}
            >
              <Typography
                variant="body2"
                color="textSecondary"
                sx={{ bgcolor: 'background.paper', marginTop: 1, textAlign: 'center' }}
              >
                Category:
              </Typography>
              {news.category.map((cat, idx) => (
                <Box
                  key={idx}
                  sx={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    bgcolor: categoryColors[cat.type]?.background || 'inherit',
                    color: 'categoryColors[cat.type]?.text' || 'inherit',
                    px: 1,
                    py: 0.5,
                    borderRadius: 1,
                  }}
                >
                  <Typography variant="body2" >{cat.name}</Typography>
                  <Box
                    sx={{
                      bgcolor: categoryColors[cat.type]?.darkBackground || 'inherit',
                      color: 'white', // Set the text color to white
                      px: 0.5,
                      py: 0.25,
                      borderRadius: 1,
                      ml: 0.5,
                    }}
                  >
                    <Typography variant="body2" sx={{color: 'white'}}>{cat.type}</Typography>
                  </Box>
                </Box>
              ))}
            </Box>
            <Typography variant="body2" gutterBottom>
              Key Points:
            </Typography>
            <ul
              style={{
                listStyle: 'none',
                padding: 0,
                margin: 0,
              }}
            >
              {news.sentences.map((sentence, sentenceIndex) => (
                <li
                  key={sentenceIndex}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    marginBottom: 8,
                  }}
                >
                  <Box
                    sx={{
                      width: 8,
                      height: 8,
                      borderRadius: '50%',
                      bgcolor: sentimentColors[news.sentiment_list[sentenceIndex]],
                      mr: 1,
                    }}
                  />
                  <Typography
                    variant="body2"
                    sx={{
                      bgcolor:
                        sentimentColors[news.sentiment_list[sentenceIndex]],
                      color: 'white',
                      px: 1,
                      py: 0.5,
                      borderRadius: 1,
                    }}
                  >
                    {sentence}
                  </Typography>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      ))}
    </Box>
  );
}

export default NewsList;