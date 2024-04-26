import React, {useState} from 'react';
import './TooLazy.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck } from '@fortawesome/free-solid-svg-icons';
import AudioTranscriber from './AudioTranscriber';
const TooLazy = () => {
  const handleTickClick = () => {
    // Empty onClick function
  };
  const [transcription, setTranscription] = useState('');
  const [url, setUrl] = useState('');
  const handleTranscribe = async (url) => {
    try {
      const response = await fetch(`http://localhost:5000/transcribe_audio?url=${encodeURIComponent(url)}`);
      if (response.ok) {
        const transcription = await response.text();
        console.log(response.text);
        setTranscription(transcription);
      } else {
        console.error('Error:', await response.text());
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };



  return (
    <div>
      
      <main>
        <h2>TOO LAZY TO VIEW THE ARTICLE OR VIDEO?</h2>
        <h2>GIVE US THE LINK.</h2>
        <div className="link-input-container">
          <input type="text" className="link-input" placeholder="Enter Youtube/article URL here... " value = {url} onChange={(e) => setUrl(e.target.value)}/>
          <FontAwesomeIcon icon={faCheck} className="tick-icon" onClick={() => {handleTranscribe(url)}} />
        </div>
        
        {transcription ? 
          <div className='aritcle-content'>
          <p>{transcription}</p>
        </div> 

        :
        <div className="article-content">
        <p>
          <strong>Price Cut on Full Self-Driving System:</strong> <span className="positive">Tesla (Company) has reduced the price of its Full Self-Driving (FSD) software by one-third to $8,000.
          (Positive)</span> This strategic in the <span className="location">US(LOC)</span> move is seen as an effort to boost adoption and customer interest ahead of the upcoming earnings release. <span className="negative">This is an example for bad news. (Negative)</span>
        </p>
      </div>
      
      
        }
        



        
          
        
      </main>
      
    </div>
  );
};

export default TooLazy;