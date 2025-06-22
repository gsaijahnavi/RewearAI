import React from "react";

export default function HistoryPage({ history }) {
  return (
    <div className="history-page">
      <h2>Outfit History</h2>
      {history.length === 0 ? (
        <div>No outfits added yet.</div>
      ) : (
        <ul>
          {history.map((outfit, idx) => (
            <li key={idx} style={{ marginBottom: 12 }}>
              <div>Top: {outfit.top}</div>
              <div>Bottom: {outfit.bottom}</div>
              {outfit.outerwear && <div>Outerwear: {outfit.outerwear}</div>}
              <div style={{ fontStyle: "italic" }}>{outfit.comment}</div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
