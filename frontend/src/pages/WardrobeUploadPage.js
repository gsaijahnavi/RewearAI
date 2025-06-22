import React, { useState, useEffect } from "react";
import { uploadWardrobeFiles } from "../api";

export default function WardrobeUploadPage({ onNext }) {
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
      await uploadWardrobeFiles(files);
      setMessage("Upload successful!");
    } catch {
      setMessage("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-form">
      <h2>Select Your Wardrobe Folder</h2>
      <input
        type="file"
        multiple
        webkitdirectory="true"
        directory="true"
        onChange={handleChange}
      />
      <button onClick={handleUpload} disabled={loading || files.length === 0}>
        {loading ? "Uploading..." : "Process Wardrobe"}
      </button>
      {message && <div className="upload-message">{message}</div>}
      {message === "Upload successful!" && (
        <button onClick={onNext} style={{ marginTop: "1rem" }}>Next: Chatbot</button>
      )}
    </div>
  );
}
