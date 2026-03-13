import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# Global cache for model and index
_cached_model = None
_cached_index = None
_cached_docs = None

INDEX_FILE = "faiss_index.bin"
DOC_FILE = "documents.pkl"

def get_model():
    global _cached_model
    if _cached_model is None:
        _cached_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _cached_model

def build_index(texts):
    model = get_model() # Use the cached model
    embeddings = model.encode(texts, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, INDEX_FILE)
    with open(DOC_FILE, "wb") as f:
        pickle.dump(texts, f)

def load_index():
    global _cached_index, _cached_docs
    if _cached_index is not None:
        return _cached_index, _cached_docs
        
    try:
        if os.path.exists(INDEX_FILE) and os.path.exists(DOC_FILE):
            _cached_index = faiss.read_index(INDEX_FILE)
            with open(DOC_FILE, "rb") as f:
                _cached_docs = pickle.load(f)
            return _cached_index, _cached_docs
    except Exception:
        pass
    return None, []

def search(query, k=5):
    index, docs = load_index()
    if index is None or len(docs) == 0:
        return []
    
    model = get_model()
    vector = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(vector, k)
    results = []
    for i in indices[0]:
        if i >= 0 and i < len(docs):
            results.append(docs[i])
    return results