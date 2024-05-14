import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  CardHeader,
  CircularProgress,
  Chip,
} from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';

const categoryColors = {
  LOC: { background: '#c8e6c9', text: '#388e3c', darkBackground: '#4caf50' },
  ORG: { background: '#E7F6F2', text: '#c62828', darkBackground: '#A5C9CA' },
  PER: { background: '#e1bee7', text: '#7b1fa2', darkBackground: '#9c27b0' },
  MISC: { background: '#bbdefb', text: '#1976d2', darkBackground: '#2196f3' },
};

const sentimentColors = {
  2: '#1f4260', // Blue
  1: '#67d294', // Green
  0: '#d50000', // Red
};

function NewsList() {
  const [newsList, setNewsList] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedTags, setSelectedTags] = useState([]);

  useEffect(() => {
    const storedNews = JSON.parse(localStorage.getItem('newsList'));
    if (storedNews) {
      setNewsList(storedNews);
    } else {
      console.log("Fetching news");
      fetchNews();
    }
  }, []);

  const fetchNews = async () => {
    const storedNews = JSON.parse(localStorage.getItem('newsList'));
    if (storedNews) {
      setNewsList(storedNews);
      console.log("Already have stored news");
    } else {
      setIsLoading(true);
      setError(null);

      try {
        const response = await fetch('http://127.0.0.1:5000/news');
        if (!response.ok) {
          throw new Error('Failed to fetch news data');
        }
        const data = await response.json();
        console.log(data);
        setNewsList(data);
        localStorage.setItem('newsList', JSON.stringify(data));
      } catch (error) {
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleRefreshClick = async () => {
    localStorage.removeItem('newsList');
    await fetchNews();
  };

  const handleTitleClick = (url) => {
    window.open(url, '_blank');
  };

  const getUniqueCategoryNames = () => {
    if (!newsList) {
      return [];
    }

    const categoryNames = newsList.flatMap((news) =>
      news.category ? news.category.map((cat) => cat.name) : []
    );
    return [...new Set(categoryNames)];
  };

  const handleTagClick = (tag) => {
    if (selectedTags.includes(tag)) {
      setSelectedTags(selectedTags.filter((t) => t !== tag));
    } else {
      setSelectedTags([...selectedTags, tag]);
    }
  };

  const filteredNewsList = selectedTags.length > 0
    ? newsList.filter((news) =>
        selectedTags.every((tag) =>
          news.category &&
          news.category.some((cat) => cat.name === tag)
        )
      )
    : newsList;

  return (
    <Box sx={{ maxWidth: 800, margin: '0 auto', padding: 2 }}>
      <Box display="flex" justifyContent="center" gap={5} mb={2}>
        <Typography variant="h4" gutterBottom>
          News List
        </Typography>
        <Button
          color="primary"
          onClick={handleRefreshClick}
          disabled={isLoading}
          sx={{ height: 40, width: 40, borderRadius: 20, padding: 0, margin: 0 }}
        >
          {isLoading ? <CircularProgress size={24} /> : <RefreshIcon />}
        </Button>
      </Box>
      {error && (
        <Typography variant="body1" color="error" gutterBottom>
          Error: {error}
        </Typography>
      )}
      <Box display="flex" flexWrap="wrap" gap={1} mb={2} alignItems={'center'}>
        <Typography variant="body1" fontWeight="bold">
          Filter by Tag:
        </Typography>
        {getUniqueCategoryNames().map((tag) => (
          <Chip
            key={tag}
            label={tag}
            onClick={() => handleTagClick(tag)}
            color={selectedTags.includes(tag) ? 'primary' : 'default'}
            variant={selectedTags.includes(tag) ? 'filled' : 'outlined'}
            sx={{ cursor: 'pointer', borderRadius: 1 }}
          />
        ))}
      </Box>

      {filteredNewsList.map((news, index) => (
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
                marginBottom: 1,
              }}
            >
              {news.category &&
                news.category.map((cat, idx) => (
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
                    <Typography variant="body2" sx={{ color: 'black' }}>
                      {cat.name}
                    </Typography>
                    <Box
                      sx={{
                        bgcolor: categoryColors[cat.type]?.darkBackground || 'inherit',
                        color: 'white',
                        px: 0.5,
                        py: 0.25,
                        borderRadius: 1,
                        ml: 0.5,
                      }}
                    >
                      <Typography variant="body2" sx={{ color: 'white' }}>
                        {cat.type}
                      </Typography>
                    </Box>
                  </Box>
                ))}
            </Box>
            <Typography variant="body2" gutterBottom fontSize={18} color={'black'}>
              Key Points:
            </Typography>
            <ul
              style={{
                listStyle: 'none',
                padding: 0,
                margin: 0,
              }}
            >
              {news.sentences &&
                news.sentences.map((sentence, sentenceIndex) => (
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
                        width: 7,
                        height: 8,
                        borderRadius: '50%',
                        bgcolor: sentimentColors[news.sentiment_list ? news.sentiment_list[sentenceIndex] : 0],
                        mr: 2,
                      }}
                    />
                    <Typography
                      variant="body1"
                      sx={{
                        bgcolor: sentimentColors[news.sentiment_list ? news.sentiment_list[sentenceIndex] : 0],
                        color: 'white',
                        px: 1,
                        py: 0.5,
                        borderRadius: 1,
                        fontSize: 18,
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