import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <header>
        <h1>FinHub</h1>
        <nav>
        <a href="/">Market Sentiment</a>
        <a href="/too-lazy">Too Lazy?</a>
        <a href="/top-news">Top News</a>
        </nav>
    </header>
      
  );
};

export default Header;