import React, { useState } from "react";
import { uploadWardrobe } from "../api";

function WardrobeUpload() {
  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFiles(Array.from(e.target.files));
  };

  const handleUpload = async () => {
    setLoading(true);
    setMessage("");
    try {
      const res = await uploadWardrobe(files);
      setMessage(res.message);
    } catch {
      setMessage("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="wardrobe-upload">
      <h2>Upload Your Wardrobe</h2>
      <input type="file" multiple onChange={handleChange} />
      <button onClick={handleUpload} disabled={loading || files.length === 0}>
        {loading ? "Uploading..." : "Upload"}
      </button>
      {message && <div className="upload-message">{message}</div>}
    </div>
  );
}

export default WardrobeUpload;
