import React from "react";

function OutfitMontage({ recommendation, montageUrl }) {
  // montageUrl is a placeholder; in a real app, you would fetch the montage image from the backend
  return (
    <div className="outfit-montage">
      <h2>Today's Outfit</h2>
      {montageUrl ? (
        <img src={montageUrl} alt="Outfit Montage" style={{ maxWidth: "100%" }} />
      ) : (
        <div>
          <pre>{JSON.stringify(recommendation, null, 2)}</pre>
        </div>
      )}
      {recommendation.comment && <div className="montage-comment">{recommendation.comment}</div>}
    </div>
  );
}

export default OutfitMontage;
