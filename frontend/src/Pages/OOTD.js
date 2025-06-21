import './OOTD.css';
import { useState } from 'react';

function OOTD() {
  const [userInput, setUserInput] = useState('');
  const [selectedStyle, setSelectedStyle] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const outfitMap = {
    "Date": {
      image: "/IMG_0970.jpg",
      description: "Soft & cute for romantic vibes "
    },
    "Hip": {
      image: "/IMG_0971.jpg",
      description: "Bold street look for confident energy "
    },
    "Clean": {
      image: "/IMG_0969.jpg",
      description: "Clean, modern, always fresh "
    }
  };

const detectStyle = (text) => {
  const lower = text.toLowerCase();

  if (
    lower.includes("date") ||
    lower.includes("love") ||
    lower.includes("romantic")
  ) {
    return "Date";
  }

  if (
    lower.includes("street") ||
    lower.includes("hip") ||
    lower.includes("freedom") ||
    lower.includes("funky")
  ) {
    return "Hip";
  }

  if (
    lower.includes("clean") ||
    lower.includes("minimal") ||
    lower.includes("neat") ||
    lower.includes("casual")
  ) {
    return "Clean";
  }

  return "Date"; // default if nothing matches
};


  const handleGenerate = () => {
    if (!userInput.trim()) return;
    setIsLoading(true);
    setSelectedStyle(null);
    const style = detectStyle(userInput);
    setTimeout(() => {
      setSelectedStyle(style);
      setIsLoading(false);
    }, 1500);
  };

  return (
    <div className="ootd-page light-theme">
      <div className="top-section">
        <h2>What’s your vibe today? 🪄</h2>
        <input
          className="ootd-input"
          placeholder="Why is your mood?"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
        />
        <button
          className="generate-btn"
          onClick={handleGenerate}
          disabled={isLoading || !userInput.trim()}
        >
          {isLoading ? 'Loading...' : 'Generate OOTD'}
        </button>
      </div>

      <div className="result-section">
        {isLoading ? (
          <div className="loader" />
        ) : selectedStyle ? (
          <div className="fade-in">
            <h3 className="style-title">{selectedStyle}</h3>
            <p className="style-description">{outfitMap[selectedStyle].description}</p>
            <img
              className="style-image"
              src={outfitMap[selectedStyle].image}
              alt={selectedStyle}
            />
          </div>
        ) : (
          <p className="placeholder-text">Try writing something short and click the button!









</p>
        )}
      </div>
    </div>
  );
}

export default OOTD;
