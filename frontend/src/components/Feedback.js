import React, { useState } from "react";
import { sendFeedback } from "../api";

function Feedback() {
  const [feedback, setFeedback] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    try {
      const res = await sendFeedback(feedback);
      setMessage(res.message);
      setFeedback("");
    } catch {
      setMessage("Failed to send feedback");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="feedback-form" onSubmit={handleSubmit}>
      <h2>Feedback</h2>
      <textarea value={feedback} onChange={e => setFeedback(e.target.value)} placeholder="Your feedback..." required />
      <button type="submit" disabled={loading}>{loading ? "Sending..." : "Send Feedback"}</button>
      {message && <div className="feedback-message">{message}</div>}
    </form>
  );
}

export default Feedback;
