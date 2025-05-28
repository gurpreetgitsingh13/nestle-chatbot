import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# === Load content and index ===
with open("scraper/nestle_cleaned_full_embedded.json") as f:
    data = json.load(f)

texts = [item["text"] for item in data]
links = [item["url"] for item in data]

index = faiss.read_index("scraper/nestle_faiss_full.index")

# === Load model ===
model = SentenceTransformer("all-MiniLM-L6-v2")  # Updated model name

# === Search logic ===
def search_nestle(query, top_k=3):
    print(f"🔍 Searching for: {query}")
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding).astype("float32"), top_k)

    results = []
    for i in I[0]:
        if i < len(texts):
            result_text = texts[i].strip().replace("\n", " ")
            results.append(f"• {result_text[:250]}...\n{links[i]}")
    return "\n\n---\n\n".join(results)

# === Run directly for testing ===
if __name__ == "__main__":
    query = input("Enter your query: ")
    print(search_nestle(query))
