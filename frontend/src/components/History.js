import React from "react";

function History({ history }) {
  return (
    <div className="history">
      <h2>Outfit History</h2>
      {history && history.length > 0 ? (
        <ul>
          {history.map((outfit, idx) => (
            <li key={idx}>{outfit.join(", ")}</li>
          ))}
        </ul>
      ) : (
        <div>No history yet.</div>
      )}
    </div>
  );
}

export default History;
