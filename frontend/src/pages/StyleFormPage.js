import React, { useState, useEffect } from "react";

export default function StyleFormPage({ onNext, initialValues }) {
  const [bio1, setBio1] = useState(initialValues?.bio1 || "");
  const [bio2, setBio2] = useState(initialValues?.bio2 || "");
  const [bio3, setBio3] = useState(initialValues?.bio3 || "");
  const [city, setCity] = useState(initialValues?.city || "");

  useEffect(() => {
    if (initialValues) {
      setBio1(initialValues.bio1 || "");
      setBio2(initialValues.bio2 || "");
      setBio3(initialValues.bio3 || "");
      setCity(initialValues.city || "");
    }
  }, [initialValues]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onNext({ bio1, bio2, bio3, city });
  };

  return (
    <form className="page-form" onSubmit={handleSubmit}>
      <h2>Tell us about your style</h2>
      <input value={bio1} onChange={e => setBio1(e.target.value)} placeholder="Style preference 1" required />
      <input value={bio2} onChange={e => setBio2(e.target.value)} placeholder="Style preference 2" required />
      <input value={bio3} onChange={e => setBio3(e.target.value)} placeholder="Style preference 3" required />
      <input value={city} onChange={e => setCity(e.target.value)} placeholder="City" required />
      <button type="submit">Next: Upload Wardrobe</button>
    </form>
  );
}
