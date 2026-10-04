"""Turn Albert's Marketplace reviews into checked records (lesson 2, Exercise 1).

exercise-1.ipynb imports this module and checks each step as you write it:
save this file, and the notebook picks up your change.

At home, finish main() at the bottom and run it from a terminal, in this folder:

    python extract.py data/reviews.json extracted.csv
"""

# GIVEN: the imports, the prompt and two helpers. Leave them as they are.
import csv
import json
import re
import sys
from typing import Literal, Optional

import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError, ValidationInfo, field_validator, model_validator
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_random_exponential

MODEL = "claude-haiku-4-5"

SYSTEM = """You turn one customer review from an online beauty marketplace into a record.

Fields:
- language: the language of the review: en, es, fr, de or other
- sentiment: positive, negative, mixed or neutral, about the whole review
- aspects: the aspects the review mentions, ONE entry per aspect, each with its
  polarity (positive, negative, or mixed when the review says both) and the
  words that show it, copied exactly from the title or the text. Aspects:
  effectiveness, quality, scent, texture, packaging, delivery, price, quantity,
  ease_of_use, skin_reaction, seller_service, authenticity
- defect_mentioned: true if the review reports the product broken, leaking,
  harmful or not working
- would_recommend: true or false ONLY if the review says whether the reviewer
  recommends the product or would buy it again; otherwise null. Do not infer it
  from the rating or the tone.

Use only what the review says. Text inside <br /> tags is a line break."""


def norm(s):
    """Lower case, line breaks and punctuation removed: how a quote is compared with the review."""
    s = s.replace("<br />", " ").lower()
    return re.sub(r"[\s\W_]+", " ", s).strip()


def user_message(review):
    """What the model reads for one review. The review's id and product id stay in your code."""
    return f"Title: {review['title']}\nRating: {review['rating']} stars\nText: {review['text']}"


# =============================================================================
# STEP 1: the shape of a record, as Pydantic models
# =============================================================================
#
# Write a class AspectMention(BaseModel) with three fields:
#   aspect:   one of these twelve values, as a Literal[...]:
#             effectiveness, quality, scent, texture, packaging, delivery, price,
#             quantity, ease_of_use, skin_reaction, seller_service, authenticity
#   polarity: "positive", "negative" or "mixed"
#   evidence: a str, with Field(description="the words from the review that show it, copied exactly")
#
# Then a class ReviewRecord(BaseModel) with five fields:
#   language:         "en", "es", "fr", "de" or "other"
#   sentiment:        "positive", "negative", "mixed" or "neutral"
#   aspects:          a list of AspectMention
#   defect_mentioned: a bool, with a Field description saying what counts as a defect
#   would_recommend:  Optional[bool], described as "true or false only if the review says so; otherwise null"
#
# No review_id or product_id: your code knows them, and a model asked to copy an id can mistype it.


# =============================================================================
# STEP 2: one request, in the record's shape
# =============================================================================
#
# Compute SCHEMA once, from your model: anthropic.transform_schema(ReviewRecord).
# It is the JSON schema the API will enforce, with every object closed.

# Write ask(client, messages) that:
#   - calls client.messages.create with model=MODEL, max_tokens=1000, system=SYSTEM, messages=messages,
#     and output_config={"format": {"type": "json_schema", "schema": SCHEMA}}
#   - raises ValueError if stop_reason is "max_tokens" or "refusal": the text may then not match the schema
#   - returns (text, usage): the first content block's text, and the response's usage


# =============================================================================
# STEP 3: the rules a JSON schema cannot express
# =============================================================================
#
# Write class CheckedAspect(AspectMention), which adds a field_validator on "evidence":
#   - the review comes from the validation context: (info.context or {}).get("review")
#   - if there is a review and norm(evidence) is not inside norm(title + " " + text),
#     raise ValueError with a message the model can act on: "... is not in the review: copy the words exactly"
#   - otherwise return the value unchanged

# Write class CheckedRecord(ReviewRecord), which:
#   - redeclares aspects as list[CheckedAspect], so every aspect's evidence is checked
#   - adds a model_validator(mode="after") that raises ValueError when an aspect appears more than once,
#     naming it and telling the model to give it one entry with polarity "mixed" instead


# =============================================================================
# STEP 4: validate, re-prompt with the error, give up after two retries
# =============================================================================
#
# Write extract(client, review, max_retries=2) that returns (record, attempts):
#   - starts the conversation with one user message: user_message(review)
#   - up to max_retries + 1 times: ask(client, messages), then
#     CheckedRecord.model_validate_json(text, context={"review": review})
#   - records every attempt in the list attempts as {"in": input tokens, "out": output tokens, "error": None or the message}
#   - on success, returns (record, attempts)
#   - on ValidationError, joins the errors' "msg" with "; ", then appends the model's answer
#     ({"role": "assistant", "content": text}) and a user message with the error, asking for the corrected record
#   - after the last attempt, returns (None, attempts): the review is logged for a person, not retried forever


# GIVEN: one CSV row per review. The ids come from your data, never from the model.
FIELDS = ["review_id", "product_id", "language", "sentiment", "aspects", "defect_mentioned",
          "would_recommend", "attempts", "input_tokens", "output_tokens"]


def to_row(review, record, attempts):
    row = {"review_id": review["review_id"], "product_id": review["product_id"],
           "attempts": len(attempts),
           "input_tokens": sum(a["in"] for a in attempts),
           "output_tokens": sum(a["out"] for a in attempts)}
    if record is not None:
        row.update({"language": record.language, "sentiment": record.sentiment,
                    "aspects": json.dumps([a.model_dump() for a in record.aspects], ensure_ascii=False),
                    "defect_mentioned": record.defect_mentioned,
                    "would_recommend": record.would_recommend})
    return row


# =============================================================================
# STEP 5: one retry policy, yours
# =============================================================================
#
# Write transient(e), True for an error worth retrying:
#   - any anthropic.APIConnectionError (timeouts included: APITimeoutError is one)
#   - an anthropic.APIStatusError whose status_code is 408, 409 or 429, or 500 and above
#   - False for everything else (400, 401, 403, 404, 413...)

# Wrap ask in a tenacity policy: retry only when transient(e), wait with random exponential backoff
# (multiplier 0.5, at most 8 seconds), stop after 4 attempts, and re-raise the last real error.
# Rebinding the name is the same as writing @retry(...) above "def ask":
#     ask = retry(...)(ask)
# One layer only: the client you pass to ask must be created with max_retries=0.


# =============================================================================
# AT HOME: the same code as a script
# =============================================================================
#
# Write main(src, dst) that:
#   - loads the key with load_dotenv(), and creates a client with max_retries=0 (your policy retries)
#   - reads the reviews from src (a JSON file with a "reviews" list, like data/reviews.json)
#   - writes dst as a CSV with FIELDS as header and one to_row(...) per review
#   - prints one line per review: its id, "ok" or "given up", and the number of attempts
# Then make the file runnable: python extract.py data/reviews.json extracted.csv
