"""Review extraction client.

Extracts structured information from Albert's Marketplace product reviews with
Claude, so the product team can see what customers say about each product.

Usage:
    from review_client import extract_all
    records = extract_all(reviews)
"""

import json

import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential

client = anthropic.Anthropic(api_key="sk-ant-api03-...")

MODEL = "claude-haiku-4-5"
PRICE_PER_MTOK = 1.00  # Claude Haiku 4.5 pricing

SYSTEM = """Extract the following from the customer review:
- language
- sentiment (positive, negative, mixed or neutral)
- aspects: a list of {aspect, polarity, evidence}
- defect_mentioned (true/false)
- would_recommend (true/false/null)

Return the result as JSON only."""


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, max=30))
def call_claude(text):
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        system=SYSTEM,
        messages=[{"role": "user", "content": text}],
    )
    return response


def extract_review(review):
    if not review["text"]:
        return None
    response = call_claude(review["title"] + "\n" + review["text"])
    data = json.loads(response.content[0].text)
    tokens = response.usage.input_tokens + response.usage.output_tokens
    cost = tokens * PRICE_PER_MTOK / 1_000_000
    return data, cost


def extract_all(reviews):
    results = []
    total_cost = 0.0
    for review in reviews:
        out = extract_review(review)
        if out:
            data, cost = out
            data["review_id"] = review["review_id"]
            results.append(data)
            total_cost += cost
    print(f"Extracted {len(results)} reviews for ${total_cost:.2f}")
    return results
