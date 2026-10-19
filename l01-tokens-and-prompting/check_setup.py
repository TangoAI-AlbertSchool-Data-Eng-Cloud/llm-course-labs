"""Run once before session 1.

With an Anthropic key it costs nothing: it only counts tokens and reads a model's limits.
With an OpenRouter key, neither is available, so it sends one tiny request instead (a fraction of a cent).
"""
import os
import sys

import anthropic
from dotenv import load_dotenv

load_dotenv()
openrouter = "openrouter" in os.environ.get("ANTHROPIC_BASE_URL", "")
print("Python", sys.version.split()[0], "| anthropic", anthropic.__version__,
      "| key:", "OpenRouter" if openrouter else "Anthropic")
if openrouter and os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("With an OpenRouter key, remove the ANTHROPIC_API_KEY line from .env: the SDK would send that key instead.")

client = anthropic.Anthropic()
question = [{"role": "user", "content": "Where is my parcel?"}]
if openrouter:
    n = client.messages.create(model="claude-haiku-4-5", max_tokens=1, messages=question).usage.input_tokens
    print(f"key works: 'Where is my parcel?' is {n} tokens on Claude Haiku 4.5, "
          "counted by a one-token request (OpenRouter has no free token counting)")
else:
    n = client.messages.count_tokens(model="claude-haiku-4-5", messages=question).input_tokens
    info = client.models.retrieve("claude-haiku-4-5")
    print(f"key works: 'Where is my parcel?' is {n} tokens on Claude Haiku 4.5, "
          f"whose context window is {info.max_input_tokens:,} tokens")
print("ready")
