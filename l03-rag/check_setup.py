"""Run once before session 3. Downloads the embedding model (about 470 MB, once), then checks
everything the lesson uses. With an Anthropic key it costs nothing: the key is checked by counting tokens,
which is free. With an OpenRouter key, which has no token counting, it sends one tiny request (a fraction of a cent)."""
import os                                 # read environment variables
import sys                                # the Python version, and stopping with a message
import time                               # a clock, to time the model's loading

print("Python", sys.version.split()[0])   # printed first: if an import below fails, you still see the version
# This lesson's packages. If one of these lines fails, that package is not installed (the setup page, section 2).
import faiss                              # the vector index
import numpy as np                        # arrays of numbers
import pypdf                              # reads PDFs
import sentence_transformers              # embedding models
import torch                              # the library the embedding model runs on
from sentence_transformers import SentenceTransformer

print("torch", torch.__version__, "| sentence-transformers", sentence_transformers.__version__,
      "| faiss", faiss.__version__, "| pypdf", pypdf.__version__)

t0 = time.time()                          # start the clock
model = SentenceTransformer("intfloat/multilingual-e5-small")  # downloaded the first time, then local
print(f"model loaded in {time.time() - t0:.0f} s: reads at most {model.max_seq_length} tokens")

# Two questions with the same meaning, in English and French, turned into vectors of length 1
a, b = model.encode(["query: How long do I have to return a product?",
                     "query: Combien de temps ai-je pour retourner un produit ?"], normalize_embeddings=True)
# Their cosine: close to 1 means the model understood they mean the same thing
print(f"cosine(English, French) = {float(np.dot(a, b)):.2f}")

index = faiss.IndexFlatIP(len(a))         # an index for vectors of this length
index.add(np.asarray([a, b], dtype="float32"))   # store the two vectors
print("faiss index:", index.ntotal, "vectors")

import anthropic                          # Anthropic's SDK: the client that calls Claude
from dotenv import load_dotenv            # reads the .env file that holds your key

load_dotenv()                             # put the key from .env into the environment
# Which kind of key: an OpenRouter .env sets ANTHROPIC_BASE_URL to OpenRouter's address
openrouter = "openrouter" in os.environ.get("ANTHROPIC_BASE_URL", "")
# Both kinds of key at once: the SDK would send the Anthropic one to OpenRouter, and fail. Stop and say so.
if openrouter and os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("With an OpenRouter key, remove the ANTHROPIC_API_KEY line from .env: the SDK would send that key instead.")
client = anthropic.Anthropic()            # the client finds the key in the environment by itself
question = [{"role": "user", "content": "Where is my parcel?"}]   # a one-message conversation
if openrouter:
    # OpenRouter has no free token counting: ask for ONE output token, and read the input count from usage
    n = client.messages.create(model="claude-haiku-4-5", max_tokens=1, messages=question).usage.input_tokens
else:
    # An Anthropic key: count the tokens, for free
    n = client.messages.count_tokens(model="claude-haiku-4-5", messages=question).input_tokens
print(f"key works ({'OpenRouter' if openrouter else 'Anthropic'}): 'Where is my parcel?' is {n} tokens on Claude Haiku 4.5")
print("ready")                            # every step above worked
