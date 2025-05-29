from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json
import re
from fastapi.responses import JSONResponse
from pathlib import Path

# === Load custom responses ===
with open("/Users/gurpreetsingh/Desktop/Nestle/backend/custom_responses.json") as f:
    custom_responses = json.load(f)

def clean_snippet(text):
    words = text.split()
    seen = set()
    cleaned_words = []
    for word in words:
        if word not in seen:
            seen.add(word)
            cleaned_words.append(word)
    cleaned = " ".join(cleaned_words)
    cleaned = re.sub(r"[^\w\s]", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:300] + "..." if len(cleaned) > 300 else cleaned

# === Load FAISS index ===
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
print("🔁 Loading FAISS index...")
index = faiss.read_index("scraper/nestle_faiss_full.index")
with open("scraper/nestle_cleaned_full_embedded.json") as f:
    docs = json.load(f)

# === FastAPI App Setup ===
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@app.post("/chat")
def chat(req: QueryRequest):
    user_query = req.query.lower()

    # === Custom Response Matching ===
    for keyword, entry in custom_responses.items():
        if keyword in user_query:
            return {
                "query": req.query,
                "results": [{
                    "title": "Custom Response",
                    "url": "",
                    "snippet": entry["response"]
                }]
            }

    # === FAISS Vector Search as fallback ===
    query_vec = model.encode([req.query])
    D, I = index.search(np.array(query_vec), k=req.top_k)

    results = []
    for score, idx in zip(D[0], I[0]):
        doc = docs[idx]
        results.append({
            "title": doc["title"],
            "url": doc["url"],
            "snippet": clean_snippet(doc["text"])
        })

    if results:
        return {"query": req.query, "results": results}
    else:
        return JSONResponse(status_code=200, content={
            "query": req.query,
            "results": [],
            "message": "Sorry, I couldn't find anything relevant."
        })
