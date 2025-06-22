const API_BASE = "http://localhost:8000";

export async function getRecommendation(data) {
  const res = await fetch(`${API_BASE}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to get recommendation");
  return res.json();
}

export async function uploadWardrobe(folderPath) {
  const res = await fetch(`${API_BASE}/upload_wardrobe`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ folder_path: folderPath }),
  });
  if (!res.ok) throw new Error("Failed to upload wardrobe");
  return res.json();
}

export async function getHistory() {
  const res = await fetch(`${API_BASE}/outfit_history`);
  if (!res.ok) throw new Error("Failed to load history");
  return res.json();
}

export async function sendFeedback(feedback) {
  const formData = new FormData();
  formData.append("feedback", feedback);
  const res = await fetch(`${API_BASE}/feedback`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error("Failed to send feedback");
  return res.json();
}
