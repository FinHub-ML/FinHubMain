import React, { useState } from 'react';

const AudioTranscriber = () => {
  const [transcription, setTranscription] = useState('');

  const handleTranscribe = async (url) => {
    try {
      const response = await fetch(`https://finhubbackend-d373ec68f9ce.herokuapp.com/transcribe_audio?url=${encodeURIComponent(url)}`);
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
      <input type="text" placeholder="Enter YouTube video URL" onBlur={(e) => handleTranscribe(e.target.value)} />
      <h2>Transcription:</h2>
      <p>{transcription}</p>
    </div>
  );
};

export default AudioTranscriber;