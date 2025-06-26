# RewearAI
Your smart personal stylist that helps you reimagine outfits from your own wardrobe tailored to weather and occasion.

## 📋 Project Overview

RewearAI is an AI-driven digital wardrobe platform that:

* **Ingests** user product photos and generates image embeddings.
* **Enriches** clothing metadata and builds recommendations with LLMs.
* **Creates** visual montages and a web-based UI for browsing and styling.

This repository contains the back-end scripts, front-end application, sample data, and configuration needed to run ClosetVerse end-to-end.

---

## 🗂️ Directory Structure

```
├── .vscode/                      # IDE settings and launch configurations
├── Sample_Images/                # Sample garment images for prototyping
├── frontend/                     # React Native / web UI source code
├── .gitignore                    # Files and folders to ignore in Git
├── 01_create_metadata_embeddings.py  # Build CLIP embeddings & save metadata
├── 02_llm.py                     # LLM-based recommendation prototype
├── 03_new_llm.py                 # Updated LLM prompting & chaining logic
├── create_montage.py             # Combine garment images into style collages
├── app.py                        # FastAPI entrypoint for backend services
├── clip_image_embeddings.npy     # Precomputed CLIP embeddings (numpy array)
├── clip_image_metadata.json      # Corresponding metadata for each embedding
└── README.md                     # This documentation file
```

---

## 🛠️ Usage

### 1. Generate Image Embeddings & Metadata

```bash
python 01_create_metadata_embeddings.py \
  --input-dir Sample_Images/ \
  --output-embeddings clip_image_embeddings.npy \
  --output-metadata clip_image_metadata.json
```

### 2. Run LLM Prototype

```bash
python 02_llm.py
# or for updated logic
python 03_new_llm.py
```

### 3. Create Garment Montage

```bash
python create_montage.py \
  --embeddings clip_image_embeddings.npy \
  --metadata clip_image_metadata.json \
  --output montage.png
```

✨ Key Features

Automatic Closet Ingestion

One-tap sync with Gmail/Outlook for receipt parsing and OAuth connections to Amazon, Shopify, and other retailers.

Vision-based add: snap a photo of a garment to auto-tag brand, category, color, and style embedding.

AI-Powered Daily Stylist

"Today’s Fit" notifications every morning use GPT-driven insights, local weather, calendar context, and your closet inventory.

Simple chat interface to ask for outfit ideas by occasion or mood.

Social OOTD Feed

Vertical photo/video posts auto-tag garments from your closet.

Likes, comments, saves, and hashtag challenges fuel community engagement.

One-Tap Resale Marketplace

Every item has structured metadata and past OOTD images—tap “Sell” to list with price suggestions and buyer trust indicators.

Integrated payment & shipping via Stripe Connect.

Sustainability & Analytics

Wear-count tracking, cost-per-wear metrics, and "carbon saved" badges highlight under-utilized items and encourage smarter shopping.

Gap analysis surfaces missing essentials and suggests affiliate products to complete your wardrobe.



