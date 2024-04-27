import React, { useState } from 'react';

const ImageGenerator = () => {
  const [prompt, setPrompt] = useState('');
  const [generatedImage, setGeneratedImage] = useState(null);

  const handleGenerate = async () => {
    try {
      const formData = new FormData();
      formData.append('prompt', prompt);
      // Add other parameters here if needed

      const response = await fetch('http://localhost:5000/generate_image', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);
        setGeneratedImage(imageUrl);
      } else {
        console.error('Error:', await response.text());
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Enter prompt..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button onClick={handleGenerate}>Generate Image</button>
      {generatedImage && <img src={generatedImage} alt="Generated" />}
    </div>
  );
};

export default ImageGenerator;