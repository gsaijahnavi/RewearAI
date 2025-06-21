import os
import json
import numpy as np
import openai
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer
from create_montage import show_outfit_montage
import requests
# ── 0. CONFIG ─────────────────────────────────────────────────────────────────
# os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")

OPENWEATHER_KEY = '04471ccf8500d004f5818580138d04d2'
MODEL = "gpt-4-turbo"

def get_weather_by_city(api_key, city):
    """
    Fetches weather data for a given city using the OpenWeather API.
    Returns the JSON response or None on failure.
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    url = f"{base_url}q={city}&appid={api_key}&units=metric"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError as e:
        code = resp.status_code
        if code == 401:
            print("Unauthorized: check your OpenWeather API key.")
        elif code == 404:
            print(f"City not found: {city}")
        else:
            print(f"HTTP error: {e}")
    except Exception as e:
        print(f"Error fetching weather: {e}")
    return None

def parse_weather(data):
    """
    Extracts temperature (°F), humidity (%), wind_speed (m/s),
    and a textual description, returns a dict.
    """
    # OpenWeather returns temp in °C; convert to °F if you need °F:
    c = data["main"]["temp"]
    temperature_f = c * 9/5 + 32

    return {
        "temperature": round(temperature_f, 1),
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "condition": data["weather"][0]["description"]
    }

# ── 2. LOAD EMBEDDINGS + METADATA ──────────────────────────────────────────────

embeddings = np.load("clip_image_embeddings.npy")           # shape (N, D)
with open("clip_image_metadata.json") as f:
    metadata = json.load(f)                                # list of dicts

# ── 3. DUMMY CONTEXT ───────────────────────────────────────────────────────────

user_bio = { 
    "bio1": "prefers neutral tones",
    "bio2": "avoids tight clothes",
    "bio3": "likes layering in colder weather"
}

# ── 4. RETRIEVE + PROMPT BUILDING ──────────────────────────────────────────────

def retrieve_candidates(query: str, k: int = 10):
    clip = SentenceTransformer("clip-ViT-B-32")
    q_emb = clip.encode(query, convert_to_tensor=True).cpu().numpy()
    sims = (embeddings @ q_emb) / (norm(embeddings, axis=1) * norm(q_emb) + 1e-8)
    idxs = np.argsort(sims)[-k:][::-1]
    return [ metadata[i]["item_id"] for i in idxs ]

def build_prompt(query: str, candidates: list, weather: dict, feedback: str = None):
    msgs = [
        {"role": "system", "content":
            "You are an AI stylist. You must ONLY choose from the provided item ID section. "
            "Return a JSON object with keys `top`, `bottom`, `outerwear` along with ids "
            "and a `comment` explaining your choice."
        },
        {"role": "user", "content": (
            f"Style preferences:\n"
            f"- {user_bio['bio1']}\n"
            f"- {user_bio['bio2']}\n"
            f"- {user_bio['bio3']}\n\n"
            f"Weather: {weather['temperature']}°F, {weather['condition']}; "
            f"Humidity: {weather['humidity']}%; Wind: {weather['wind_speed']} m/s\n\n"
            f"Available item IDs: {', '.join(candidates)}"
        )}
    ]
    # zero-shot examples omitted for brevity...
    msgs.append({"role": "user", "content": f"Query: \"{query}\""})
    if feedback:
        msgs.append({"role": "user", "content":
                     f"Feedback: {feedback}. Please revise only the relevant part, "
                     "still using only the provided item IDs."})
    return msgs

def ask_stylist(prompt_messages):
    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=prompt_messages,
        temperature=0,
        max_tokens=200
    )
    return resp.choices[0].message.content

# ── 5. MAIN ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # 1) Dynamic city (hard-coded for now)
    city = "Boston"

    # 2) Fetch & parse
    raw = get_weather_by_city(OPENWEATHER_KEY, city)
    if not raw:
        raise RuntimeError("Failed to fetch weather—check your API key & network.")
    weather = parse_weather(raw)

    # 3) Build + retrieve + ask stylist
    user_query = "Can you suggest a party dress for today?"
    candidates = retrieve_candidates(user_query, k=10)
    prompt = build_prompt(user_query, candidates, weather)
    suggestion = ask_stylist(prompt)
    print("Stylist suggestion:\n", suggestion)

    # 4) Display montage
    suggestion_dict = json.loads(suggestion)
    with open("clip_image_metadata.json", "r") as f:
        metadata_store = json.load(f)

    show_outfit_montage(
        suggestion=suggestion_dict,
        metadata_store=metadata_store,
        image_size=(200, 200),
        title=f"Outfit for {city}"
    )