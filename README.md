# RewearAI
Your smart personal stylist that helps you reimagine outfits from your own wardrobe tailored to weather and occasion.

## 📋 Project Overview

ClosetVerse is an AI-driven digital wardrobe platform that:

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

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* Node.js 16+ & npm (for the frontend)
* Git CLI
* Access to GPU (optional, for faster embedding generation)

### Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/your-org/closetverse.git
   cd closetverse
   ```

2. **Setup Python environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate       # Windows
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**

   ```bash
   cd frontend
   npm install
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

### 4. Start Backend Server

```bash
uvicorn app:app --reload
```

Open your browser at `http://localhost:8000/docs` to explore the API.

### 5. Launch Frontend App

```bash
cd frontend
npm start
```

Follow prompts to run on iOS/Android simulator or web environment.

---

## 🔧 Configuration

* **app.py** reads environment variables for API keys:

  * `OPENAI_API_KEY` — your OpenAI credential for LLM calls
  * `CLIP_MODEL` — model name for embedding (e.g., `openai/clip-vit-base-patch32`)
* **frontend/.env** (create if missing) for any client-side keys (e.g., maps, auth)

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add awesome feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request.

Please follow the existing code style and include tests where applicable.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
