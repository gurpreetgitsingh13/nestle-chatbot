import json
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# === Load cleaned full-site data ===
with open("scraper/nestle_cleaned_full.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df = df[df['text'].str.len() > 50].reset_index(drop=True)
texts = df['text'].tolist()

print(f"✅ Loaded {len(texts)} valid documents.")

# === Load smaller, stable model ===
print("🧠 Loading model...")
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # ✅ lighter + stable

# === Generate embeddings safely ===
print("⚙️ Generating embeddings...")
embeddings = model.encode(
    texts,
    show_progress_bar=True,
    batch_size=4,                  # ✅ small batch
    normalize_embeddings=True,
    use_multiprocessing=False      # ✅ no multiprocessing
)
embeddings = np.array(embeddings).astype("float32")

# === Create FAISS index ===
print("📦 Building FAISS index...")
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# === Save index and associated data ===
faiss.write_index(index, "scraper/nestle_faiss_full.index")
df.to_json("scraper/nestle_cleaned_full_embedded.json", orient="records", indent=2)

print("✅ Embeddings saved to FAISS index.")
