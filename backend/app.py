from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json

# === Load model and index once ===
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

print("🔁 Loading FAISS index...")
index = faiss.read_index("scraper/nestle_faiss_full.index")

with open("scraper/nestle_cleaned_full_embedded.json") as f:
    docs = json.load(f)

# === FastAPI Setup ===
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with your frontend origin if needed
    allow_methods=["*"],
    allow_headers=["*"]
)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@app.post("/chat")
def chat(req: QueryRequest):
    query_vec = model.encode([req.query])
    D, I = index.search(np.array(query_vec), k=req.top_k)

    results = []
    for score, idx in zip(D[0], I[0]):
        if score < 0.4:  # adjust if needed
            doc = docs[idx]
            results.append({
                "title": doc.get("title", "No title"),
                "url": doc.get("url", "#"),
                "snippet": " ".join(dict.fromkeys(doc["text"].split()))[:300]
            })

    if not results:
        return {
            "query": req.query,
            "results": [{
                "title": "Sorry!",
                "url": "#",
                "snippet": "I couldn’t find any relevant Nestlé content for that. Try rephrasing or ask about a specific product or recipe."
            }]
        }

    return {"query": req.query, "results": results}
