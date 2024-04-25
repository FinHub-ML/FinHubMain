import React from 'react';
import './FloatingKeywords.css';
const FloatingKeywords = ({ keywords }) => {
    
  return (
    <div className="floating-keywords">
      {keywords.map((keyword, index) => (
        <span
          key={index}
          className="keyword"
          style={{
            animationDelay: `${index * 0.5}s`,
            animationDuration: `${10 + index * 2}s`,
            left: `${40 + Math.cos((index * 2 * Math.PI) / keywords.length) * 30}%`,
            top: `${40 + Math.sin((index * 2 * Math.PI) / keywords.length) * 30}%`,
          }}
        >
          {keyword}
        </span>
      ))}
    </div>
  );
};

export default FloatingKeywords;