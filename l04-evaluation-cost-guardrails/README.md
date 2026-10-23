# Lesson 4: evaluation, cost and guardrails

| File | What it is |
|---|---|
| `demo.ipynb` | The demo, with the outputs it printed when the teacher ran it. Run it again and compare: your numbers will differ |
| `exercise-1.ipynb`, `evaluate.py` | Exercise 1, in class, in pairs: the evaluation harness. The notebook checks each function of `evaluate.py` as you write it |
| `rag_system.py` | The system under test: lesson 3's help-centre assistant, finished and defended. GIVEN: you do not edit it |
| `requirements.txt` | Lesson 3's packages, plus `sacrebleu` and `rouge-score`, pinned to the versions the demo ran with |
| `data/golden.json` | The golden set: 25 questions with answers a person checked against the help centre |
| `data/05-product-pages-injected.pdf` | The product pages as one seller edited them (lesson 3's injection) |

**Setup:** lesson 3's environment, then, in this folder, environment active:
`pip install -r requirements.txt`. Copy your `.env` from lesson 1's folder
into this one: the notebooks read the key from the folder they run in. The
help centre's PDFs are downloaded by `rag_system.py` from the company's public
release, once, into `data/policy-corpus/` (ignored by Git), and checked
against their published checksums.

**In the exercise notebook**, cells whose first line is `# GIVEN:` run as they
are. Every other code cell holds only comments: they say what to write, and you
write the code under each one. In `evaluate.py`, the same rule holds for each
`STEP`.

**On Google Colab:** upload the notebook, `rag_system.py` and, for Exercise 1,
`evaluate.py`; add your key under *Secrets*, named `ANTHROPIC_API_KEY` for an
Anthropic key or `OPENROUTER_API_KEY` for an OpenRouter key; then uncomment
the notebook's first code cell and run it before any other.

**Cost of one full run:** the demo about $0.32 (two thirds of it on Claude
Sonnet 5.5), Exercise 1 about $0.08 in class and $0.25 for the part at home. The embeddings are free: they
run on your machine.
