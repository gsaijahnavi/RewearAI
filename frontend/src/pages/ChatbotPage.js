import React, { useState, useEffect } from "react";
import { getRecommendation, sendFeedback } from "../api";

// Helper to load metadata
async function fetchMetadata() {
  const res = await fetch("http://localhost:8000/load_wardrobe");
  if (!res.ok) return [];
  const data = await res.json();
  return data.metadata || [];
}

function getImagePathsFromSuggestion(suggestion, metadata) {
  if (!suggestion) return [];
  const ids = [suggestion.top, suggestion.bottom, suggestion.outerwear].filter(Boolean);
  return ids.map(id => {
    const meta = metadata.find(m => m.id === id || m.item_id === id);
    if (!meta) return null;
    // Find 'Sample_Images' in path, get relative path, ensure no leading slash
    const idx = meta.image_path.indexOf("Sample_Images");
    if (idx === -1) return null;
    let rel = meta.image_path.substring(idx + "Sample_Images".length);
    if (rel.startsWith("/")) rel = rel.substring(1);
    return `http://localhost:8000/images/${encodeURI(rel)}`;
  }).filter(Boolean);
}

function replaceItemIdsWithNames(comment, metadata, suggestion, weather) {
  if (!comment) return comment;
  let result = comment;
  // Build a map from id to item name
  const idToName = {};
  metadata.forEach(m => {
    idToName[m.id] = m.item;
    idToName[m.item_id] = m.item; // support both
  });
  // Replace all item_XX or item_id with item name
  Object.entries(suggestion).forEach(([key, val]) => {
    if (key === 'comment' || !val) return;
    const name = idToName[val];
    if (name) {
      // Replace all occurrences of the id with the name (case-insensitive)
      const regex = new RegExp(val, 'gi');
      result = result.replace(regex, name);
    }
  });
  // Append temperature if available
  if (weather && weather.temperature) {
    result += ` (Current temperature: ${weather.temperature}\u00B0F)`;
  }
  return result;
}

export default function ChatbotPage({ styleInfo, onAddToHistory }) {
  const [query, setQuery] = useState("");
  const [chat, setChat] = useState([]);
  const [recommendation, setRecommendation] = useState(null);
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(false);
  const [feedbackLoading, setFeedbackLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [metadata, setMetadata] = useState([]);
  const [weather, setWeather] = useState(null);

  useEffect(() => {
    fetchMetadata().then(setMetadata);
  }, []);

  // Fetch weather from last recommendation
  useEffect(() => {
    if (recommendation && chat.length > 0) {
      const lastStylist = chat.filter(m => m.type === 'stylist').slice(-1)[0];
      if (lastStylist && lastStylist.weather) setWeather(lastStylist.weather);
    }
  }, [recommendation, chat]);

  const handleQuery = async () => {
    setLoading(true);
    const req = {
      bio1: styleInfo.bio1,
      bio2: styleInfo.bio2,
      bio3: styleInfo.bio3,
      city: styleInfo.city,
      user_query: query,
      outfit_history: history.length > 0 ? history : undefined,
      feedback: undefined
    };
    try {
      const res = await getRecommendation(req);
      setRecommendation(res.suggestion);
      setWeather(res.weather);
      setChat([
        ...chat,
        { type: "user", text: query },
        { type: "stylist", ...res.suggestion, weather: res.weather }
      ]);
    } catch {
      setChat([
        ...chat,
        { type: "user", text: query },
        { type: "error", text: "Could not get recommendation." }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async () => {
    setFeedbackLoading(true);
    const req = {
      bio1: styleInfo.bio1,
      bio2: styleInfo.bio2,
      bio3: styleInfo.bio3,
      city: styleInfo.city,
      user_query: query,
      outfit_history: history.length > 0 ? history : undefined,
      feedback: feedback
    };
    try {
      const res = await getRecommendation(req);
      setRecommendation(res.suggestion);
      setWeather(res.weather);
      setChat([
        ...chat,
        { type: "user", text: feedback },
        { type: "stylist", ...res.suggestion, weather: res.weather }
      ]);
    } catch {
      setChat([
        ...chat,
        { type: "user", text: feedback },
        { type: "error", text: "Could not update recommendation." }
      ]);
    } finally {
      setFeedbackLoading(false);
    }
  };

  // Collage rendering for stylist messages
  function StylistCollage({ suggestion }) {
    const imagePaths = getImagePathsFromSuggestion(suggestion, metadata);
    if (imagePaths.length === 0) return null;
    // All images: same height, width auto, object-fit contain, background white
    const imgStyle = {
      height: 140,
      width: "auto",
      objectFit: "contain",
      background: "#fff",
      borderRadius: 8,
      border: "1px solid #ccc",
      display: "block"
    };
    return (
      <div style={{ display: "flex", gap: 8, margin: "8px 0", alignItems: "center" }}>
        {imagePaths.map((src, idx) => (
          <div key={idx} style={{ width: 120, height: 140, display: "flex", alignItems: "center", justifyContent: "center", background: "#fff" }}>
            <img
              src={src}
              alt="outfit"
              style={imgStyle}
            />
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="chatbot-page">
      <h2>Ask for an Outfit</h2>
      <input value={query} onChange={e => setQuery(e.target.value)} placeholder="What do you need an outfit for?" />
      <button onClick={handleQuery} disabled={loading || !query}>{loading ? "Loading..." : "Ask Stylist"}</button>
      <div className="chat-window">
        {chat.map((msg, idx) =>
          msg.type === "user" ? (
            <div key={idx} className="chat-user">You: {msg.text}</div>
          ) : msg.type === "stylist" ? (
            <div key={idx} className="chat-stylist">
              <div><b>Stylist:</b></div>
              <StylistCollage suggestion={msg} />
              <div style={{ fontStyle: "italic", marginTop: 4 }}>
                {replaceItemIdsWithNames(msg.comment, metadata, msg, msg.weather || weather)}
              </div>
            </div>
          ) : (
            <div key={idx} className="chat-error">{msg.text}</div>
          )
        )}
      </div>
      {recommendation && (
        <div className="feedback-section">
          <textarea value={feedback} onChange={e => setFeedback(e.target.value)} placeholder="Feedback (e.g. change top, prefer lighter color, etc)" />
          <button onClick={handleFeedback} disabled={feedbackLoading || !feedback}>{feedbackLoading ? "Updating..." : "Send Feedback"}</button>
          <button onClick={() => { onAddToHistory(recommendation); setHistory([...history, recommendation]); }} style={{ marginLeft: 8 }}>Add to History</button>
        </div>
      )}
    </div>
  );
}
