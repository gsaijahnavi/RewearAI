import React, { useState } from "react";
import { getRecommendation } from "../api";

function RecommendationForm({ setRecommendation, setHistory }) {
  const [bio1, setBio1] = useState("");
  const [bio2, setBio2] = useState("");
  const [bio3, setBio3] = useState("");
  const [city, setCity] = useState("");
  const [userQuery, setUserQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = {
        bio1, bio2, bio3, city, user_query: userQuery,
      };
      const res = await getRecommendation(data);
      setRecommendation(res.suggestion);
      setHistory(res.candidates || []);
    } catch (err) {
      setError("Could not get recommendation");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="recommend-form" onSubmit={handleSubmit}>
      <h2>Get Your Outfit Recommendation</h2>
      <input value={bio1} onChange={e => setBio1(e.target.value)} placeholder="Style preference 1" required />
      <input value={bio2} onChange={e => setBio2(e.target.value)} placeholder="Style preference 2" required />
      <input value={bio3} onChange={e => setBio3(e.target.value)} placeholder="Style preference 3" required />
      <input value={city} onChange={e => setCity(e.target.value)} placeholder="City" required />
      <input value={userQuery} onChange={e => setUserQuery(e.target.value)} placeholder="What do you need an outfit for?" required />
      <button type="submit" disabled={loading}>{loading ? "Loading..." : "Get Recommendation"}</button>
      {error && <div className="error">{error}</div>}
    </form>
  );
}

export default RecommendationForm;
