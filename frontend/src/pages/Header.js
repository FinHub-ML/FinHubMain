import React from 'react';
import './Header.css';
import { Link } from 'react-router-dom';
const Header = () => {
  return (
    <header>
        <Link to="/"> <h1>FinHub</h1></Link>
        <nav>
        <Link to="/">Market Sentiment</Link>
        <Link to="/too-lazy">Too Lazy?</Link>
        <Link to="/top-news">Top News</Link>
        </nav>
    </header>
      
  );
};

export default Header;