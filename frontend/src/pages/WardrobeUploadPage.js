import React, { useState, useEffect } from "react";
import { uploadWardrobe } from "../api";

export default function WardrobeUploadPage({ onNext, folderPath, setFolderPath }) {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [localPath, setLocalPath] = useState(folderPath || "");

  useEffect(() => {
    setLocalPath(folderPath || "");
  }, [folderPath]);

  const handleUpload = async () => {
    setLoading(true);
    setMessage("");
    try {
      await uploadWardrobe(localPath);
      setMessage("Upload successful!");
      setFolderPath(localPath);
    } catch {
      setMessage("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-form">
      <h2>Enter Your Wardrobe Folder Path</h2>
      <input
        type="text"
        value={localPath}
        onChange={e => setLocalPath(e.target.value)}
        placeholder="/Users/yourname/path/to/wardrobe"
      />
      <button onClick={handleUpload} disabled={loading || !localPath}>
        {loading ? "Processing..." : "Process Wardrobe"}
      </button>
      {message && <div className="upload-message">{message}</div>}
      {message === "Upload successful!" && (
        <button onClick={onNext} style={{ marginTop: "1rem" }}>Next: Chatbot</button>
      )}
    </div>
  );
}
