import React, { useState } from "react";
import Stepper from "./Stepper";
import StyleFormPage from "./pages/StyleFormPage";
import WardrobeUploadPage from "./pages/WardrobeUploadPage";
import ChatbotPage from "./pages/ChatbotPage";
import HistoryPage from "./pages/HistoryPage";
import "./App.css";

function App() {
  const [step, setStep] = useState(0);
  const [styleInfo, setStyleInfo] = useState(null);
  const [history, setHistory] = useState([]);
  // For preserving wardrobe folder path
  const [wardrobePath, setWardrobePath] = useState("");

  // Navigation helpers
  const nextStep = () => setStep(s => Math.min(s + 1, 3));
  const prevStep = () => setStep(s => Math.max(s - 1, 0));

  return (
    <div className="app-container">
      <h1>RewearAI Stylist</h1>
      <Stepper step={step} />
      {step === 0 && (
        <>
          <StyleFormPage
            onNext={info => { setStyleInfo(info); nextStep(); }}
            initialValues={styleInfo}
          />
        </>
      )}
      {step === 1 && (
        <>
          <WardrobeUploadPage
            onNext={nextStep}
            folderPath={wardrobePath}
            setFolderPath={setWardrobePath}
          />
          <button onClick={nextStep} disabled={!wardrobePath}>Next</button>
        </>
      )}
      {step === 2 && (
        <>
          <ChatbotPage
            styleInfo={styleInfo}
            onAddToHistory={outfit => { setHistory([...history, outfit]); }}
          />
          <button onClick={nextStep}>Next</button>
        </>
      )}
      {step === 3 && (
        <>
          <HistoryPage history={history} />
        </>
      )}
    </div>
  );
}

export default App;
