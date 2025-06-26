import React from "react";

export default function Stepper({ step }) {
  const steps = ["Style Info", "Wardrobe Upload", "Chatbot", "History"];
  return (
    <div style={{ display: "flex", justifyContent: "center", margin: "1rem 0" }}>
      {steps.map((label, idx) => (
        <div key={label} style={{
          padding: "0.5rem 1.5rem",
          borderBottom: step === idx ? "3px solid #4a4a8a" : "1px solid #ccc",
          color: step === idx ? "#4a4a8a" : "#888",
          fontWeight: step === idx ? "bold" : "normal"
        }}>{label}</div>
      ))}
    </div>
  );
}
