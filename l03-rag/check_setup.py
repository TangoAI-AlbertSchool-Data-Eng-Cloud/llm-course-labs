"""Run once before session 3. Downloads the embedding model (about 470 MB, once), then checks
everything the lesson uses. Costs nothing: the key is checked by counting tokens, which is free."""
import sys
import time

print("Python", sys.version.split()[0])
import faiss
import numpy as np
import pypdf
import sentence_transformers
import torch
from sentence_transformers import SentenceTransformer

print("torch", torch.__version__, "| sentence-transformers", sentence_transformers.__version__,
      "| faiss", faiss.__version__, "| pypdf", pypdf.__version__)

t0 = time.time()
model = SentenceTransformer("intfloat/multilingual-e5-small")  # downloaded the first time, then local
print(f"model loaded in {time.time() - t0:.0f} s: reads at most {model.max_seq_length} tokens")

a, b = model.encode(["query: How long do I have to return a product?",
                     "query: Combien de temps ai-je pour retourner un produit ?"], normalize_embeddings=True)
print(f"cosine(English, French) = {float(np.dot(a, b)):.2f}")

index = faiss.IndexFlatIP(len(a))
index.add(np.asarray([a, b], dtype="float32"))
print("faiss index:", index.ntotal, "vectors")

import anthropic
from dotenv import load_dotenv

load_dotenv()
n = anthropic.Anthropic().messages.count_tokens(
    model="claude-haiku-4-5", messages=[{"role": "user", "content": "Where is my parcel?"}]).input_tokens
print(f"key works: 'Where is my parcel?' is {n} tokens on Claude Haiku 4.5")
print("ready")
