import os
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from sentence_transformers import SentenceTransformer
import re
import json

# Load CLIP model from sentence-transformers
model = SentenceTransformer("clip-ViT-B-32")

# Image preprocessing (CLIP expected format)
preprocess = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.4815, 0.4578, 0.4082],
                         std=[0.2686, 0.2613, 0.2758])
])

root_dir = "Sample_Images"
metadata_store = []
embeddings_store = []
item_count = 0

for category_folder in os.listdir(root_dir):
    category_path = os.path.join(root_dir, category_folder)
    if os.path.isdir(category_path):
        for fname in os.listdir(category_path):
            if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                fpath = os.path.join(category_path, fname)
                category = category_folder
                item_name = os.path.splitext(fname)[0]
                item_list = item_name.lower()
                item_name = re.sub(r'\d+', '', item_name).lower().strip()
                item_id = f"item_{item_count}"
                item_count += 1
                try:
                    image = Image.open(fpath).convert("RGB")
                    with torch.no_grad():
                        embedding = model.encode([image], convert_to_tensor=True).cpu().numpy()
                    embeddings_store.append(embedding[0])
                    metadata_store.append({
                        "id": item_id,
                        "image_path": fpath,
                        "category": category,
                        "item": item_name,
                        "item_id": item_list
                    })
                except Exception as e:
                    print(f"Error processing {fpath}: {e}")

# Save embeddings and metadata
np.save("clip_image_embeddings.npy", np.array(embeddings_store))
with open("clip_image_metadata.json", "w") as f:
    json.dump(metadata_store, f, indent=2)

print(f"Saved {len(embeddings_store)} embeddings and metadata.")

