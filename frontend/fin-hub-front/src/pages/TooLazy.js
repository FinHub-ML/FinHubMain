import React, { useState } from 'react';
import './TooLazy.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck, faSpinner } from '@fortawesome/free-solid-svg-icons';

const TooLazy = () => {
  const [transcription, setTranscription] = useState('');
  const [summary, setSummary] = useState({ keyPoints: [], entities: [] });
  const [url, setUrl] = useState('');
  const [isTranscribingLoading, setIsTranscribingLoading] = useState(false);
  const [isSummarizingLoading, setIsSummarizingLoading] = useState(false);

  const handleTranscribe = async (url) => {
    setIsTranscribingLoading(true);
    setTranscription('');
    setSummary({ keyPoints: [], entities: [] });

    try {
      const response = await fetch(`http://localhost:5000/transcribe_audio?url=${encodeURIComponent(url)}`);
      if (response.ok) {
        const transcription = await response.text();
        setTranscription(transcription);
        setIsTranscribingLoading(false);
        fetchSummary(transcription);
      } else {
        console.error('Error:', await response.text());
        setIsTranscribingLoading(false);
      }
    } catch (error) {
      console.error('Error:', error);
      setIsTranscribingLoading(false);
    }
  };

  const fetchSummary = async (transcription) => {
    setIsSummarizingLoading(true);
    try {
      const summaryResponse = await fetch('http://localhost:5000/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: transcription }),
      });

      if (summaryResponse.ok) {
        const { key_points, entities } = await summaryResponse.json();
        setSummary({
          keyPoints: key_points,
          entities: entities,
        });
      } else {
        console.error('Error:', await summaryResponse.text());
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsSummarizingLoading(false);
    }
  };
  const highlightEntities = (text, entities) => {
    // Create a map to store unique entities with their types to avoid duplicates
    const entityMap = new Map(entities.map(([name, type]) => [name, type]));

    // Sort entities by length in descending order to handle nested entities correctly (longest first)
    const sortedEntities = Array.from(entityMap).sort((a, b) => b[0].length - a[0].length);

    // Escape special characters in entity names for use in regular expressions
    sortedEntities.forEach(([name, type], index) => {
        const { bgColor, textColor } = getEntityColor(type);
        const escapedName = escapeRegExp(name);
        const regex = new RegExp(`\\b${escapedName}\\b`, 'g');

        text = text.replace(regex, (match) => {
            return `<span style="background-color: ${bgColor}; padding: 2px 4px; border-radius: 4px; margin-right: 4px;">
                        ${match}</span>
                    <span style="background-color: ${textColor}; color: white; padding: 2px 4px; border-radius: 4px;">
                        ${type}</span>`;
        });
    });

    return text;
  };

  const escapeRegExp = (text) => {
      return text.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&');
  };

  const getEntityColor = (type) => {
      switch (type) {
          case 'LOC':
              return { bgColor: 'lightblue', textColor: 'darkblue' };
          case 'ORG':
              return { bgColor: 'lightpink', textColor: 'darkred' };
          default:
              return { bgColor: 'transparent', textColor: 'grey' };
      }
  };


  return (
    <div>
      <main>
        <h2>TOO LAZY TO VIEW THE ARTICLE OR VIDEO?</h2>
        <h2>GIVE US THE LINK.</h2>
        <div className="link-input-container">
          <input
            type="text"
            className="link-input common-text-style" // Apply common styles to input as well
            placeholder="Enter Youtube/article URL here..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <FontAwesomeIcon icon={faCheck} className="tick-icon" onClick={() => handleTranscribe(url)} />
        </div>
        <div className="article-content">
          {isTranscribingLoading ? (
            <div className="loading-spinner common-text-style">
              <FontAwesomeIcon icon={faSpinner} spin />
              <span>Transcribing...</span>
            </div>
          ) : (
            transcription && (
              <p className="common-text-style" dangerouslySetInnerHTML={{ __html: highlightEntities(transcription, summary.entities) }} />
            )
          )}
          {isSummarizingLoading ? (
            <div className="loading-spinner common-text-style">
              <FontAwesomeIcon icon={faSpinner} spin />
              <span>Summarizing...</span>
            </div>
          ) : (
            <>
              {summary.keyPoints && summary.keyPoints.length > 0 ? (
                <>
                  <h2>Key Points</h2>
                  <ul>
                  {summary.keyPoints.map((point, index) => (
                    <li className="common-text-style" key={index} dangerouslySetInnerHTML={{ __html: highlightEntities(point, summary.entities) }} />
                  ))}
                  </ul>
                </>
                
              ) : (<> </>)}
              
              {summary.entities && summary.entities.length > 0 ? (
                <> 
                <h2>Entities</h2>
                <ul>
                  {summary.entities.map(([name, type], index) => (
                    <li className="common-text-style" key={index}>
                      {name} ({type})
                    </li>
                  ))}
                </ul>

                </>
              ) : (<> </>)}
            </>
          )}
        </div>
      </main>
    </div>
  );
};

export default TooLazy;
