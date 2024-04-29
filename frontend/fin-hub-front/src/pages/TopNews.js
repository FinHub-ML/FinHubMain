import React, { useState } from 'react';

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

  return (
    <div>
      <h1>News List</h1>
      <button onClick={fetchNews} disabled={isLoading}>
        {isLoading ? 'Loading...' : 'Fetch News'}
      </button>
      {error && <div>Error: {error}</div>}
      {newsList.map((news, index) => (
        <div key={index}>
          <h2>{news.title}</h2>
          <p>URL: {news.url}</p>
          <p>
            Category:{' '}
            {news.category.map((cat, idx) => (
              <span key={idx}>
                {cat.name} ({cat.type}){' '}
              </span>
            ))}
          </p>
          <p>Sentences:</p>
          <ul>
            {news.sentences.map((sentence, sentenceIndex) => (
              <li key={sentenceIndex}>
                {sentence} (Sentiment: {news.sentiment_list[sentenceIndex]})
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

export default NewsList;