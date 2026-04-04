#!/usr/bin/env python3
"""Alpha Memory - Smart semantic memory search using BGE-M3 embeddings."""
import sys
import os
import json
import requests
import glob
from pathlib import Path

# Embedding endpoint (via Cloudflare tunnel)
EMBEDDING_URL = "https://lm-studio.tacimpulse.net/v1/embeddings"
EMBEDDING_MODEL = "text-embedding-bge-m3"

# Reranker endpoint
RERANKER_URL = "https://lm-studio.tacimpulse.net/v1/embeddings"
RERANKER_MODEL = "text-embedding-bge-reranker-v2-m3"

# Memory files
WORKSPACE = "/root/.openclaw/workspace"
MEMORY_FILES = [
    "MEMORY.md",
    "USER.md",
    "SOUL.md",
    "IDENTITY.md",
]
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
VECTOR_STORE = os.path.join(WORKSPACE, "memory_vectors.json")

def get_embedding(text):
    """Get embedding for a text string."""
    resp = requests.post(
        EMBEDDING_URL,
        json={"model": EMBEDDING_MODEL, "input": text},
        timeout=30
    )
    if resp.status_code == 200:
        return resp.json()["data"][0]["embedding"]
    return None

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x ** 2 for x in a) ** 0.5
    norm_b = sum(x ** 2 for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0
    return dot / (norm_a * norm_b)

def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks."""
    chunks = []
    lines = text.split('\n')
    current_chunk = ""
    
    for line in lines:
        if len(current_chunk) + len(line) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Keep overlap
            current_chunk = current_chunk[-overlap:] + "\n" + line
        else:
            current_chunk += "\n" + line
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

def load_memory_files():
    """Load all memory files and chunk them."""
    chunks = []
    
    # Load main memory files
    for filename in MEMORY_FILES:
        filepath = os.path.join(WORKSPACE, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                text = f.read()
            for chunk in chunk_text(text):
                chunks.append({"text": chunk, "source": filename})
    
    # Load daily memory files
    if os.path.exists(MEMORY_DIR):
        for filepath in sorted(glob.glob(os.path.join(MEMORY_DIR, "*.md"))):
            with open(filepath, 'r') as f:
                text = f.read()
            for chunk in chunk_text(text):
                chunks.append({"text": chunk, "source": os.path.basename(filepath)})
    
    return chunks

def build_vector_store():
    """Build or rebuild the vector store from memory files."""
    chunks = load_memory_files()
    print(f"Found {len(chunks)} chunks from memory files")
    
    vector_store = []
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk["text"])
        if embedding:
            vector_store.append({
                "text": chunk["text"],
                "source": chunk["source"],
                "embedding": embedding
            })
            print(f"  Embedded chunk {i+1}/{len(chunks)}: {chunk['source']}")
    
    with open(VECTOR_STORE, 'w') as f:
        json.dump(vector_store, f)
    
    print(f"Vector store saved: {len(vector_store)} entries")
    return vector_store

def search_memory(query, top_k=5):
    """Search memory using semantic similarity."""
    # Load or build vector store
    if os.path.exists(VECTOR_STORE):
        with open(VECTOR_STORE, 'r') as f:
            vector_store = json.load(f)
    else:
        vector_store = build_vector_store()
    
    if not vector_store:
        return []
    
    # Get query embedding
    query_embedding = get_embedding(query)
    if not query_embedding:
        return []
    
    # Calculate similarities
    results = []
    for entry in vector_store:
        sim = cosine_similarity(query_embedding, entry["embedding"])
        results.append({
            "text": entry["text"],
            "source": entry["source"],
            "score": sim
        })
    
    # Sort by similarity
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return results[:top_k]

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  alpha-memory.py build          # Rebuild vector store")
        print("  alpha-memory.py search <query> # Search memory")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "build":
        build_vector_store()
    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: alpha-memory.py search <query>")
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        results = search_memory(query)
        print(f"\nSearch results for: {query}\n")
        for i, r in enumerate(results):
            print(f"[{i+1}] (score: {r['score']:.3f}, source: {r['source']})")
            print(f"    {r['text'][:200]}...")
            print()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
