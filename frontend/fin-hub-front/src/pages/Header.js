import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <header>
        <a href = "/"> <h1>FinHub</h1></a>
        <nav>
        <a href="/">Market Sentiment</a>
        <a href="/too-lazy">Too Lazy?</a>
        <a href="/top-news">Top News</a>
        </nav>
    </header>
      
  );
};

export default Header;