"""Measure the help-centre assistant: scores, a judge, cost and a cache (lesson 4, Exercise 1).

exercise-1.ipynb imports this module and checks each step as you write it: save this file, and the
notebook picks up your change. The system it measures is rag_system.py, which you do not edit.
"""

# GIVEN: the imports, the models, the prices, and the judge's prompts. Leave them as they are.
import hashlib
import json
import re
import time

import sacrebleu
from pydantic import BaseModel
from rouge_score import rouge_scorer

HAIKU_45, HAIKU_55, SONNET = "claude-haiku-4-5", "claude-haiku-5-5", "claude-sonnet-5-5"
# The judge: Claude Haiku 5.5, because it is cheap enough to grade every answer in class. Its flaw: Haiku 5.5
# is also one of the two variants it grades, so for half the answers the judge grades its own model's work.
# A different and stronger model, Claude Sonnet 5.5, is the better control: the notebook tries it at home.
JUDGE = HAIKU_55

# $ per million tokens, input and output, Anthropic's pricing page, checked 14 October 2026
PRICE = {HAIKU_45: (1.00, 5.00), HAIKU_55: (0.10, 0.50), SONNET: (2.00, 10.00)}
CACHE_WRITE = 1.25                                            # a 5-minute cache write, times the input price
CACHE_READ = {HAIKU_45: 0.10, HAIKU_55: 0.10, SONNET: 0.05}   # a cache read, times the input price

POINTWISE = """You grade answers given by a customer assistant of an online marketplace.
Compare the candidate answer with the reference answer, which is correct. Score the candidate from 1 to 5:
5 = correct and complete; 4 = correct, missing a minor detail; 3 = partly correct;
2 = mostly wrong; 1 = wrong or contradicts the reference. Give a short reason, then the score."""

PAIRWISE = """You compare two answers given by a customer assistant of an online marketplace to the same
question, against the reference answer, which is correct. Say which answer is better: "A" or "B".
Give a short reason, then your choice."""


class Score(BaseModel):
    reason: str
    score: int


class Choice(BaseModel):
    reason: str
    better: str


# =============================================================================
# STEP 1: exact match and token F1, with SQuAD's normalisation (6 minutes)
# =============================================================================
#
# Write normalise(text), the rule both scores apply first:
#   - lower case, and the € sign replaced by a space
#   - a decimal comma between two digits becomes a point: "4,90" -> "4.90"     re.sub(r"(\d),(\d)", r"\1.\2", s)
#   - a space before "%" after a digit goes: "12 %" -> "12%"                   re.sub(r"(\d)\s+%", r"\1%", s)
#   - a full stop becomes a space, unless it sits inside a number              re.sub(r"(?<!\d)\.|\.(?!\d)", " ", s)
#   - every other character that is not a letter, a digit, "." or "%" becomes a space   re.sub(r"[^\w.% ]", " ", s)
#   - then split into words, drop "a", "an" and "the", and join the rest with single spaces

# Write exact_match(prediction, gold): True when the two texts are equal once normalised.

# Write token_f1(prediction, gold), SQuAD's F1 over words:
#   - p and g: the two normalised texts, split into words
#   - if either is empty: 1.0 when both are, 0.0 otherwise
#   - common: for each distinct word of p, the smaller of its counts in p and in g, summed
#   - if common is 0, return 0.0
#   - precision = common / len(p), recall = common / len(g); return 2 * precision * recall / (precision + recall)


# =============================================================================
# STEP 2: BLEU and ROUGE-L, from their libraries (4 minutes)
# =============================================================================
#
# Write bleu(candidate, reference): sacrebleu's sentence BLEU, from 0 to 100.
#   sacrebleu.sentence_bleu(candidate, [reference]).score       (the reference goes in a list)

# Write rouge_l(candidate, reference): ROUGE-L's F-measure, times 100.
#   rouge_scorer.RougeScorer(["rougeL"]).score(reference, candidate)["rougeL"].fmeasure    (the reference FIRST)


# =============================================================================
# STEP 3: a model as judge, and the swap (10 minutes)
# =============================================================================
#
# Write judge(client, item, candidate, model=JUDGE): one pointwise verdict, and what it cost in tokens.
#   - one call to client.messages.parse with model=model, max_tokens=4000, system=POINTWISE, output_format=Score,
#     and one user message whose content is three lines:
#         Question: <item["question"]>
#         Reference answer: <item["reference"]>
#         Candidate answer: <candidate>
#   - return two things: the parsed Score (r.parsed_output) and r.usage

# Write judge_pair(client, item, a, b, model=JUDGE): which of two answers is better, "A" or "B".
#   - the same call with system=PAIRWISE and output_format=Choice, the user message being:
#         Question: <question>
#         Reference answer: <reference>
#         (an empty line) Answer A: <a>
#         (an empty line) Answer B: <b>
#   - return the first letter of parsed_output.better, stripped and in upper case

# Write swap(client, item, first, second, model=JUDGE): the pair judged twice, once in each order.
#   - once = judge_pair(..., first, second), then twice = judge_pair(..., second, first)
#   - return "first" if `first` won both times (A, then B), "second" if `second` won both times (B, then A),
#     and "position" when the same letter won both times: then the ORDER decided, not the answers


# =============================================================================
# STEP 4: what a call cost (6 minutes)
# =============================================================================
#
# Write cost(model, usage, count_output=True): the call's price in dollars, prices per million tokens in PRICE:
#     usage.input_tokens                 x the input price
#   + usage.cache_creation_input_tokens  x the input price x CACHE_WRITE
#   + usage.cache_read_input_tokens      x the input price x CACHE_READ[model]
#   + usage.output_tokens                x the output price      (left out when count_output is False)
#   all divided by 1,000,000. The two cache fields can be None, or missing: count them as 0
#   (getattr(usage, "cache_read_input_tokens", 0) or 0).


# =============================================================================
# STEP 5: an answer cache with a SHA-256 key (6 minutes)
# =============================================================================
#
# Write key(model, system, question): the SHA-256 of everything that changes the answer.
#   json.dumps({"model": model, "system": system, "question": question}, sort_keys=True), encoded to bytes,
#   hashed with hashlib.sha256, returned as .hexdigest() (64 characters)

# Write the class AnswerCache, which answers a repeated request from memory instead of calling the API.
#   - __init__(self, ask): keep ask, the function that really calls the model (rag_system.ask); an empty dict
#     self.store; two counters, self.calls and self.hits, at 0
#   - get(self, client, model, system, question): returns (answer, usage, ms)
#       - k = key(model, system, question)
#       - if k is in self.store: count a hit, and return the stored answer, None for the usage (nothing was
#         billed) and the milliseconds the lookup took
#       - otherwise: answer, usage, ms = self.ask(client, model, system, question); count a call; store the
#         answer under k; return (answer, usage, ms)


# =============================================================================
# STEP 6: one golden item through the system, scored (8 minutes)
# =============================================================================
#
# Write evaluate_item(client, centre, item, model, cache): returns one row, a dict.
#   - passages = centre.retrieve(item["question"]); system = centre.prompt(passages)
#   - answer, usage, ms = cache.get(client, model, system, item["question"])
#   - verdict, judge_usage = judge(client, item, answer.answer)
#   - return a dict with:
#       "id": item["id"], "answer": answer.answer, "short_answer": answer.short_answer,
#       "evidence": centre.has_evidence(item, passages),
#       "em": exact_match(answer.short_answer, item["short"]), "f1": token_f1(answer.short_answer, item["short"]),
#       "score": verdict.score, "right": verdict.score >= 4,
#       "usd": cost(model, usage) (0.0 when usage is None: the cache answered), "ms": ms,
#       "judge_usd": cost(JUDGE, judge_usage)
#   For the three questions the help centre does not answer, item["short"] is "": an empty short answer is right.
