import os
import json
import numpy as np
import openai
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer
from create_montage import show_outfit_montage

# ── 0. CONFIG ─────────────────────────────────────────────────────────────────
os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")


MODEL = "gpt-4-turbo"

# ── 1. LOAD EMBEDDINGS + METADATA ──────────────────────────────────────────────
embeddings = np.load("clip_image_embeddings.npy")           # shape (N, D)
with open("clip_image_metadata.json") as f:
    metadata = json.load(f)                                # list of dicts


##################### DUMMY DATA FOR TESTING #####################
# ──  CONTEXT DATA ────────────────────────────────────────────────────────────

# 1. Example user preferences
user_bio = { 
    "bio1": "prefers neutral tones",
    "bio2": "avoids tight clothes",
    "bio3": "likes layering in colder weather"
}

# 2. Weather data (in a real app, get this from a weather API)
weather = {"temperature": 55, "condition": "rainy"} 

# 3. Occasion
occasion = "formal event"  # e.g., "casual outing", "business meeting"

# 4. Recent outfits worn by the user

outfit_history = [ 
    {"date": "2025-06-20", "items": ["blazer2", "shirt2", "pants1"]},
    {"date": "2025-06-19", "items": ["skirt1", "shirt1"]},
]

# 5. Zero-shot examples for the LLM
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

# ── 3. RETRIEVE TOP-K VIA CLIP SIMILARITY ────────────────────────────────────────
def retrieve_candidates(query: str, k: int = 10):
    clip = SentenceTransformer("clip-ViT-B-32")
    q_emb = clip.encode(query, convert_to_tensor=True).cpu().numpy()
    sims = (embeddings @ q_emb) / (norm(embeddings, axis=1) * norm(q_emb) + 1e-8)
    idxs = np.argsort(sims)[-k:][::-1]
    return [ metadata[i]["item"] for i in idxs ]


def build_prompt(query: str, candidates: list, feedback: str = None):
    """
    candidates: a list of your actual item_id values (e.g. ["puffer1","trench1",...])
    """
    msgs = [
        {"role": "system", "content":
            "You are an AI stylist. You must ONLY choose from the provided item IDs. "
            "Do NOT invent generic terms like “outerwear” or “top” — use exactly one of the IDs. "
            "Return a JSON object with keys `top`, `bottom`, `outerwear` along with ids"
            "and a `comment` explaining your choice."
        },
        {"role": "user", "content": (
            f"Style preferences:\n"
            f"- {user_bio['bio1']}\n"
            f"- {user_bio['bio2']}\n"
            f"- {user_bio['bio3']}\n\n"
            f"Weather: {weather['temperature']}°F, {weather['condition']}\n\n"
            f"Recent outfits: {', '.join(outfit_history[-2]['items'])}\n\n"
            f"Available item IDs: {', '.join(candidates)}"
        )}
    ]

    # zero-shot examples also use real item_ids
    for ex in zero_shot_examples:
        msgs.append({"role": "user",      "content": f"Query: \"{ex['query']}\""})
        msgs.append({"role": "assistant", "content": json.dumps(ex["outfit"])})

    # the actual user query
    msgs.append({"role": "user", "content": f"Query: \"{query}\""})

    # optional feedback for an iteration
    if feedback:
        msgs.append({
            "role": "user",
            "content": f"Feedback: {feedback}. Please revise only the relevant part, "
                       "still using only the provided item IDs."
        })

    return msgs



# ── 5. ASK THE LLM ─────────────────────────────────────────────────────────────
def ask_stylist(prompt_messages):
    resp = openai.chat.completions.create(
      model=MODEL,
      messages=prompt_messages,
      temperature=0,
      max_tokens=200
    )
    return resp.choices[0].message.content

# ── 6. PUT IT ALL TOGETHER ────────────────────────────────────────────────────
if __name__ == "__main__":
    user_query = "Can you suggest a rainy outfit for today?"
    print("User query:", user_query)

    
    # 1) retrieve
    candidates = retrieve_candidates(user_query, k=10)
    # 2) build prompt
    prompt = build_prompt(user_query, candidates)
    # 3) get suggestion
    suggestion = ask_stylist(prompt)
    print("Initial suggestion:\n", suggestion)

    # 4) simulate feedback
    print("\n-- User says: I don't like the outerwear --")
    prompt2 = build_prompt(user_query, candidates, feedback="I don't like the outerwear")
    suggestion2 = ask_stylist(prompt2)
    print("Revised suggestion:\n", suggestion2)

    suggestion2_dict = json.loads(suggestion2)

    # load your metadata_store (same as before)
    with open("clip_image_metadata.json", "r") as f:
        metadata_store = json.load(f)

    # display the revised outfit
    show_outfit_montage(
        suggestion=suggestion2_dict,
        metadata_store=metadata_store,
        image_size=(200, 200),
        title="Revised Outfit"
    )