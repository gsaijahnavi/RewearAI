import os
import json
import numpy as np
import openai
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import requests
import glob
from PIL import Image

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY", "04471ccf8500d004f5818580138d04d2")
MODEL = "gpt-4-turbo"

# Load CLIP model and embeddings at startup
clip = SentenceTransformer("clip-ViT-B-32")
if os.path.exists("clip_image_embeddings.npy"):
    embeddings = np.load("clip_image_embeddings.npy")
else:
    embeddings = None
if os.path.exists("clip_image_metadata.json"):
    with open("clip_image_metadata.json") as f:
        metadata = json.load(f)
else:
    metadata = []

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve images from Sample_Images at /images
app.mount("/images", StaticFiles(directory="Sample_Images"), name="images")

class RecommendRequest(BaseModel):
    bio1: str
    bio2: str
    bio3: str
    city: str
    user_query: str
    outfit_history: Optional[List[List[str]]] = None
    feedback: Optional[str] = None

class WardrobeUploadResponse(BaseModel):
    message: str
    num_images: int

@app.post("/recommend")
def recommend(req: RecommendRequest):
    # 1. Weather
    def get_weather_by_city(api_key, city):
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        url = f"{base_url}q={city}&appid={api_key}&units=metric"
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return None
    def parse_weather(data):
        c = data["main"]["temp"]
        temperature_f = c * 9/5 + 32
        return {
            "temperature": round(temperature_f, 1),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "condition": data["weather"][0]["description"]
        }
    raw = get_weather_by_city(OPENWEATHER_KEY, req.city)
    if not raw:
        raise HTTPException(status_code=400, detail="Failed to fetch weather for city")
    weather = parse_weather(raw)
    # 2. Candidates
    def retrieve_candidates(query: str, k: int = 10):
        q_emb = clip.encode(query, convert_to_tensor=True).cpu().numpy()
        from numpy.linalg import norm
        sims = (embeddings @ q_emb) / (norm(embeddings, axis=1) * norm(q_emb) + 1e-8)
        idxs = np.argsort(sims)[-k:][::-1]
        return [metadata[i]["item_id"] for i in idxs]
    candidates = retrieve_candidates(req.user_query, k=20)
    # 3. Prompt and LLM
    def build_prompt(query: str, candidates: list, feedback: Optional[str] = None, prev_outfit: Optional[dict] = None):
        # Dummy outfit history for now (should be user-specific in real app)
        outfit_history = [
            {"date": "2025-06-20", "items": ["blazer2", "shirt2", "pants1"]},
            {"date": "2025-06-19", "items": ["skirt1", "shirt1"]},
        ]
        zero_shot_examples = [
            {
              "query": "What should I wear for a cold formal event?",
              "outfit": {"top":"shirt2","bottom":"pants1","outerwear":"blazer3",
                         "comment":"Layered a long-sleeve grey shirt with black pants and navy blazer for warmth & formality."}
            },
            {
              "query": "Need something casual for a sunny day",
              "outfit": {"top":"shirt1","bottom":"skirt2","outerwear":"none",
                         "comment":"Light cotton shirt and breezy skirt to stay cool in sun."}
            }
        ]
        msgs = [
            {"role": "system", "content":
                "You are an AI stylist. You must ONLY choose from the provided item ID section of "
                "Do NOT invent generic terms like “outerwear” or “top” — use exactly one of the IDs. "
                "Return a JSON object with keys `top`, `bottom`, `outerwear` along with ids"
                "and a `comment` explaining your choice."
            },
            {"role": "user", "content": (
                f"Style preferences:\n"
                f"- {req.bio1}\n"
                f"- {req.bio2}\n"
                f"- {req.bio3}\n\n"
                f"Weather: {weather['temperature']}°F, {weather['condition']}\n\n"
                f"Recent outfits: {', '.join(outfit_history[-2]['items'])}\n\n"
                f"Available item IDs: {', '.join(candidates)}"
            )}
        ]
        for ex in zero_shot_examples:
            msgs.append({"role": "user", "content": f"Query: \"{ex['query']}\""})
            msgs.append({"role": "assistant", "content": json.dumps(ex["outfit"])})
        msgs.append({"role": "user", "content": f"Query: \"{query}\""})
        if feedback and req.outfit_history and len(req.outfit_history) > 0:
            prev = req.outfit_history[-1]
            prev_outfit_dict = {"top": prev[0] if len(prev) > 0 else None, "bottom": prev[1] if len(prev) > 1 else None, "outerwear": prev[2] if len(prev) > 2 else None}
            msgs.append({
                "role": "user",
                "content": (
                    f"Previous outfit: {json.dumps(prev_outfit_dict)}\n"
                    f"Feedback: {feedback}. Please revise ONLY the part(s) mentioned in the feedback, and keep all other items exactly the same as in the previous outfit. Use only the provided item IDs."
                )
            })
        elif feedback:
            msgs.append({
                "role": "user",
                "content": f"Feedback: {feedback}. Please revise only the relevant part, still using only the provided item IDs."
            })
        return msgs

    prompt = build_prompt(req.user_query, candidates, req.feedback)
    def ask_stylist(prompt_messages):
        resp = openai.chat.completions.create(
            model=MODEL,
            messages=prompt_messages,
            temperature=0,
            max_tokens=200
        )
        return resp.choices[0].message.content
    suggestion = ask_stylist(prompt)
    suggestion_dict = json.loads(suggestion)
    return {"suggestion": suggestion_dict, "weather": weather, "candidates": candidates}

@app.post("/upload_wardrobe", response_model=WardrobeUploadResponse)
def upload_wardrobe(folder_path: str = Body(..., embed=True)):
    """
    Accepts a folder path, recursively finds all images, and processes them for embedding/metadata.
    Metadata matches the structure from 01_create_metadata_embeddings.py.
    """
    import re
    from PIL import Image
    import torch
    from torchvision import transforms

    exts = ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.webp"]
    all_files = []
    for ext in exts:
        all_files.extend(glob.glob(os.path.join(folder_path, "**", ext), recursive=True))
    if not all_files:
        return {"message": "No images found in folder.", "num_images": 0}

    preprocess = transforms.Compose([
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.4815, 0.4578, 0.4082], std=[0.2686, 0.2613, 0.2758])
    ])
    clip_model = SentenceTransformer("clip-ViT-B-32")
    embeddings = []
    metadata = []
    item_count = 0
    for img_path in all_files:
        try:
            category = os.path.basename(os.path.dirname(img_path))
            fname = os.path.basename(img_path)
            item_name = os.path.splitext(fname)[0]
            item_list = item_name.lower()
            item_name_clean = re.sub(r'\d+', '', item_name).lower().strip()
            item_id = f"item_{item_count}"
            item_count += 1
            image = Image.open(img_path).convert("RGB")
            with torch.no_grad():
                emb = clip_model.encode([image], convert_to_tensor=True).cpu().numpy()
            embeddings.append(emb[0])
            metadata.append({
                "id": item_id,
                "image_path": img_path,
                "category": category,
                "item": item_name_clean,
                "item_id": item_list
            })
        except Exception as e:
            continue
    if embeddings:
        np.save("clip_image_embeddings.npy", np.array(embeddings))
        with open("clip_image_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
    return {"message": f"Processed {len(embeddings)} images from folder.", "num_images": len(embeddings)}

@app.post("/upload_wardrobe_files", response_model=WardrobeUploadResponse)
def upload_wardrobe_files(files: List[UploadFile] = File(...)):
    """
    Accepts a list of image files uploaded from the frontend, processes them for embedding/metadata.
    Metadata matches the structure from 01_create_metadata_embeddings.py.
    """
    import re
    import shutil
    from PIL import Image
    import torch
    from torchvision import transforms

    upload_dir = os.path.join("Sample_Images", "Uploaded")
    os.makedirs(upload_dir, exist_ok=True)
    embeddings = []
    metadata = []
    item_count = 0
    clip_model = SentenceTransformer("clip-ViT-B-32")
    preprocess = transforms.Compose([
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.4815, 0.4578, 0.4082], std=[0.2686, 0.2613, 0.2758])
    ])
    for file in files:
        try:
            fname = file.filename
            save_path = os.path.join(upload_dir, fname)
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            category = os.path.basename(os.path.dirname(save_path))
            item_name = os.path.splitext(fname)[0]
            item_list = item_name.lower()
            item_name_clean = re.sub(r'\d+', '', item_name).lower().strip()
            item_id = f"item_{item_count}"
            item_count += 1
            image = Image.open(save_path).convert("RGB")
            with torch.no_grad():
                emb = clip_model.encode([image], convert_to_tensor=True).cpu().numpy()
            embeddings.append(emb[0])
            metadata.append({
                "id": item_id,
                "image_path": save_path,
                "category": category,
                "item": item_name_clean,
                "item_id": item_list
            })
        except Exception as e:
            continue
    if embeddings:
        np.save("clip_image_embeddings.npy", np.array(embeddings))
        with open("clip_image_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
    return {"message": f"Processed {len(embeddings)} images from upload.", "num_images": len(embeddings)}

@app.get("/load_wardrobe")
def load_wardrobe():
    # Return the current metadata
    return {"metadata": metadata}

@app.get("/outfit_history")
def get_outfit_history():
    # Dummy: In real app, load from DB or user profile
    return {"history": [["blazer2", "shirt2", "pants1"], ["skirt1", "shirt1"]]}

@app.post("/feedback")
def feedback_endpoint(feedback: str = Form(...)):
    # Dummy: In real app, store feedback
    return {"message": "Feedback received", "feedback": feedback}
