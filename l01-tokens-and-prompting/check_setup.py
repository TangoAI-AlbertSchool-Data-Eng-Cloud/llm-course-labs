"""Run once before session 1.

With an Anthropic key it costs nothing: it only counts tokens and reads a model's limits.
With an OpenRouter key, neither is available, so it sends one tiny request instead (a fraction of a cent).
"""
import os                               # read environment variables
import sys                              # the Python version, and stopping with a message

import anthropic                        # Anthropic's SDK: if this import fails, the packages are not installed
from dotenv import load_dotenv          # reads the .env file that holds your key

load_dotenv()                           # put the key from .env into the environment
# Which kind of key: an OpenRouter .env sets ANTHROPIC_BASE_URL to OpenRouter's address
openrouter = "openrouter" in os.environ.get("ANTHROPIC_BASE_URL", "")
print("Python", sys.version.split()[0], "| anthropic", anthropic.__version__,
      "| key:", "OpenRouter" if openrouter else "Anthropic")
# Both kinds of key at once: the SDK would send the Anthropic one to OpenRouter, and fail. Stop and say so.
if openrouter and os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("With an OpenRouter key, remove the ANTHROPIC_API_KEY line from .env: the SDK would send that key instead.")

client = anthropic.Anthropic()          # the client finds the key in the environment by itself
question = [{"role": "user", "content": "Where is my parcel?"}]   # a one-message conversation
if openrouter:
    # OpenRouter has no free token counting: ask for ONE output token, and read the input count from usage
    n = client.messages.create(model="claude-haiku-4-5", max_tokens=1, messages=question).usage.input_tokens
    print(f"key works: 'Where is my parcel?' is {n} tokens on Claude Haiku 4.5, "
          "counted by a one-token request (OpenRouter has no free token counting)")
else:
    # An Anthropic key: count the tokens (free), and read the model's limits (free)
    n = client.messages.count_tokens(model="claude-haiku-4-5", messages=question).input_tokens
    info = client.models.retrieve("claude-haiku-4-5")
    print(f"key works: 'Where is my parcel?' is {n} tokens on Claude Haiku 4.5, "
          f"whose context window is {info.max_input_tokens:,} tokens")   # `:,` writes 200,000
print("ready")                          # every step above worked
