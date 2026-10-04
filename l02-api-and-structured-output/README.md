# Lesson 2: programmatic API use and structured outputs

| File | What it is |
|---|---|
| `demo.ipynb` | The demo, with the outputs it printed when the teacher ran it. Run it again and compare: your numbers will differ |
| `exercise-1.ipynb` | Exercise 1, in class, in pairs: it runs and checks `extract.py` as you write it |
| `extract.py` | The module you write in Exercise 1: each `STEP` holds the comments that say what to write. At home it becomes a script: `python extract.py data/reviews.json extracted.csv` |
| `exercise-2.ipynb` | Exercise 2, at home: the audit of `review_client.py`, with fakes that stand in for the API |
| `review_client.py` | The client an AI assistant wrote, which Exercise 2 audits. **Do not run it with your key** |
| `requirements.txt` | The packages, pinned to the versions the demo ran with. Install them in your lesson 1 environment |
| `data/reviews.json` | Twenty of the company's reviews |
| `data/expected.json` | The same twenty as records a person checked. Exercise 1 compares against them at the end |
| `data/orders.json` | The shipments of the orders the support tickets quote, for the demo's `get_order` tool |

**Install** (in this folder, with your lesson 1 environment active):

```bash
pip install -r requirements.txt
```

**In the exercise notebooks**, cells whose first line is `# GIVEN:` run as they
are. Every other code cell holds only comments: they say what to write, and you
write the code under each one. The questions you answer in words are in the
markdown cells. In `extract.py`, the same rule holds for each `STEP`.

**On Google Colab:** upload the notebook, the `data` folder, and for
Exercise 1 `extract.py` (for Exercise 2, `review_client.py`); add your key
under *Secrets*; run
`!pip install -q anthropic==1.10.0 tenacity==9.1.4 pydantic==2.13.5 python-dotenv==1.2.4`
first.

**Cost of one full run:** the demo about $0.11, Exercise 1 about $0.05,
Exercise 2 nothing (it never calls the real API).

The reviews are from Amazon Reviews'23 (McAuley Lab, CC BY-SA 4.0), through
Albert's Marketplace's release v1.0.0; the order data is from the same release.
