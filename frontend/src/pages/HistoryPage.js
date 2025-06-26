import React, { useEffect, useState } from "react";

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
    const idx = meta.image_path.indexOf("Sample_Images");
    if (idx === -1) return null;
    let rel = meta.image_path.substring(idx + "Sample_Images".length);
    if (rel.startsWith("/")) rel = rel.substring(1);
    return {
      src: `http://localhost:8000/images/${encodeURI(rel)}`,
      label: meta.item || id
    };
  }).filter(Boolean);
}

export default function HistoryPage({ history }) {
  const [metadata, setMetadata] = useState([]);
  useEffect(() => { fetchMetadata().then(setMetadata); }, []);

  return (
    <div className="history-page">
      <h2>Outfit History</h2>
      {history.length === 0 ? (
        <div>No outfits added yet.</div>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {history.map((outfit, idx) => {
            const images = getImagePathsFromSuggestion(outfit, metadata);
            // Use date from outfit if present, else fallback to today
            let dateStr = outfit.date;
            let dateObj;
            if (dateStr) {
              dateObj = new Date(dateStr);
            } else {
              dateObj = new Date();
            }
            const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
            const dayOfWeek = days[dateObj.getDay()];
            const formatted = dateObj.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
            return (
              <li
                key={idx}
                style={{
                  marginBottom: 20,
                  border: '1px solid #e5e7eb',
                  borderRadius: 8,
                  boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
                  padding: 16,
                  cursor: 'pointer',
                  transition: 'box-shadow 0.2s',
                  background: '#fff',
                  outline: 'none',
                  userSelect: 'none',
                }}
                tabIndex={0}
                onMouseOver={e => e.currentTarget.style.boxShadow = '0 4px 16px rgba(79,70,229,0.15)'}
                onMouseOut={e => e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.06)'}
                onFocus={e => e.currentTarget.style.boxShadow = '0 4px 16px rgba(79,70,229,0.15)'}
                onBlur={e => e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.06)'}
              >
                <div style={{ fontWeight: 600, marginBottom: 8 }}>Outfit #{idx + 1}</div>
                <div style={{ color: '#666', fontSize: 14, marginBottom: 8 }}>
                  {formatted} ({dayOfWeek})
                </div>
                <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
                  {images.map((img, i) => (
                    <div key={i} style={{ width: 100, height: 120, display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#fff', border: '1px solid #eee', borderRadius: 6 }}>
                      <img src={img.src} alt={img.label} style={{ maxHeight: 110, maxWidth: 90, objectFit: 'contain' }} />
                    </div>
                  ))}
                </div>
                <div style={{ fontStyle: "italic", marginTop: 8 }}>{outfit.comment}</div>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
