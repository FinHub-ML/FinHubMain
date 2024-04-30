import React, { useState } from 'react';
import './TooLazy.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck, faSpinner } from '@fortawesome/free-solid-svg-icons';
import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import SentimentDisplay from './SentimentDisplay';

const TooLazy = () => {
  const [transcription, setTranscription] = useState('');
  const [summary, setSummary] = useState({ keyPoints: [], entities: [] });
  const [url, setUrl] = useState('');
  const [isTranscribingLoading, setIsTranscribingLoading] = useState(false);
  const [isSummarizingLoading, setIsSummarizingLoading] = useState(false);
  const [expanded, setExpanded] = useState(false);
  

  const handleChange = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
  };
  const handleTranscribe = async (url) => {
    setIsTranscribingLoading(true);
    setTranscription('');
    setSummary({ keyPoints: [], entities: [] });

    try {
      const response = await fetch(`http://127.0.0.1:5000/transcribe_audio?url=${encodeURIComponent(url)}`);
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
      const summaryResponse = await fetch('http://127.0.0.1:5000/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: transcription }),
      });

      if (summaryResponse.ok) {
        const { key_points, entities } = await summaryResponse.json();
        console.log(key_points, entities);
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
  const removeOverlappingEntities = (entities) => {
    const sortedEntities = entities.sort((a, b) => b.name.length - a.name.length);
    const uniqueEntities = [];
  
    for (const entity of sortedEntities) {
      const { name } = entity;
      const isSubstring = uniqueEntities.some(({ name: existingName }) => existingName.includes(name));
  
      if (!isSubstring) {
        uniqueEntities.push(entity);
      }
    }
  
    return uniqueEntities;
  };
  const highlightEntities = (text, entities) => {
    // Sort entities by length in descending order to handle nested entities correctly (longest first)
    const sortedEntities = entities.sort((a, b) => b.name.length - a.name.length);
  
    // Escape special characters in entity names for use in regular expressions
    let highlightedText = text;
  
    sortedEntities.forEach((entity) => {
      const { name, type } = entity;
      const { bgColor, textColor } = getEntityColor(type);
      const escapedName = escapeRegExp(name);
      const regex = new RegExp(`\\b${escapedName}\\b`, 'g');
  
      highlightedText = highlightedText.replace(regex, (match) => {
        return `<span style="background-color: ${bgColor}; padding: 2px 4px; border-radius: 4px; margin-right: 4px;">${match}</span><span style="background-color: ${textColor}; color: white; padding: 2px 4px; border-radius: 4px;">${type}</span>`;
      });
    });
  
    return highlightedText;
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
              return { bgColor: 'lightgray', textColor: 'grey' };
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
            className="link-input common-text-style"
            placeholder="Enter Youtube/article URL here..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <FontAwesomeIcon
            icon={faCheck}
            className="tick-icon"
            onClick={() => handleTranscribe(url)}
          />
        </div>
        <div className="article-content">
          {isTranscribingLoading ? (
            <div className="loading-spinner common-text-style">
              <FontAwesomeIcon icon={faSpinner} spin />
              <span>Transcribing...</span>
            </div>
          ) : (
            transcription && (
              <Accordion
                expanded={expanded === 'transcription'}
                onChange={handleChange('transcription')}
              >
                <AccordionSummary
                  expandIcon={<ExpandMoreIcon />}
                  aria-controls="transcription-content"
                  id="transcription-header"
                >
                  <Typography>Transcription</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography
                    style={{ lineHeight: '3rem' }}
                    dangerouslySetInnerHTML={{
                      __html: highlightEntities(transcription, summary.entities),
                    }}
                  />
                </AccordionDetails>
              </Accordion>
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
                <Accordion
                  expanded={expanded === 'keyPoints'}
                  onChange={handleChange('keyPoints')}
                >
                  <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="key-points-content"
                    id="key-points-header"
                  >
                    <Typography>Key Points</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                  <ul
                    style={{
                      padding: 0,
                      margin: 0,
                    }}
                  >
                    {summary.keyPoints.map((point, index) => (
                      <li
                        className="common-text-style"
                        key={index}
                        style={{
                          marginBottom: '1.5rem',
                          display: 'flex',
                          alignItems: 'center',
                        }}
                      >
                        <span dangerouslySetInnerHTML={{ __html: highlightEntities(point, summary.entities) }} />
                        <SentimentDisplay text={point} />
                      </li>
                    ))}
                  </ul>
                  </AccordionDetails>
                </Accordion>
              ) : (
                <></>
              )}
              {summary.entities && summary.entities.length > 0 ? (
                <Accordion
                  expanded={expanded === 'entities'}
                  onChange={handleChange('entities')}
                >
                  <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="entities-content"
                    id="entities-header"
                  >
                    <Typography>Tags </Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                      {Object.entries(
                        Array.from(new Set(removeOverlappingEntities(summary.entities).map(({ name, type }) => `${name} (${type})`))).sort().reduce((acc, entity) => {
                          const [nameWithType, type] = entity.split(' (');
                          const name = nameWithType.replace(` ${type}`, '');
                          const typedEntities = acc[type] || [];
                          typedEntities.push(name);
                          acc[type] = typedEntities;
                          return acc;
                        }, {})
                      ).map(([type, typedEntities]) => (
                        <div key={type} style={{ marginRight: '1rem', fontSize: 24, marginBottom: 15, fontWeight: 400}}>
                          {typedEntities.map((name, index) => (
                            <span
                              key={`${name}-${index}`}
                              style={{ marginRight: '0.5rem', }}
                              dangerouslySetInnerHTML={{
                                __html: highlightEntities(`${name}`, removeOverlappingEntities(summary.entities)),
                              }}
                            />
                          ))}
                        </div>
                      ))}
                    </div>
                  </AccordionDetails>
                </Accordion>
              ) : (
                <></>
              )}
            </>
          )}
        </div>
      </main>
    </div>
  );
};

export default TooLazy;