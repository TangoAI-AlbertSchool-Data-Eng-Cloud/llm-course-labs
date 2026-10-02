"""Run once before session 1. Costs nothing: it only counts tokens and reads a model's limits."""
import sys

import anthropic
from dotenv import load_dotenv

load_dotenv()
print("Python", sys.version.split()[0], "| anthropic", anthropic.__version__)
client = anthropic.Anthropic()
n = client.messages.count_tokens(model="claude-haiku-4-5",
                                 messages=[{"role": "user", "content": "Where is my parcel?"}]).input_tokens
info = client.models.retrieve("claude-haiku-4-5")
print(f"key works: 'Where is my parcel?' is {n} tokens on Claude Haiku 4.5, "
      f"whose context window is {info.max_input_tokens:,} tokens")
print("ready")
