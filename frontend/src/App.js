import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Home from './pages/Home';
import TooLazy from './pages/TooLazy';
import TopNews from './pages/TopNews';
import Footer from './pages/Footer';
import Header from './pages/Header';

const App = () => {
  return (
    <Router basename={process.env.PUBLIC_URL}>
      <div>
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/too-lazy" element={<TooLazy />} />
          <Route path="/top-news" element={<TopNews />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
};

export default App;