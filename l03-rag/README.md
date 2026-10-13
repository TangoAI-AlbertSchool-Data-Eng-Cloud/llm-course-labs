# Lesson 3: retrieval-augmented generation

| File | What it is |
|---|---|
| `demo.ipynb` | The demo, with the outputs it printed when the teacher ran it. Run it again and compare: your numbers will differ |
| `exercise-1.ipynb` | Exercise 1, in class, in pairs: it runs and checks `rag.py` as you write it |
| `rag.py` | The module you write in Exercise 1: each `STEP` holds the comments that say what to write. Exercise 2 imports it too |
| `exercise-2.ipynb` | Exercise 2, at home: the same pipeline on the EU AI Act, and the regulation that amended it |
| `requirements.txt` | The packages, pinned. Install them in your lesson 1 environment, **before the session**: about 1.6 GB |
| `check_setup.py` | Run once before session 3: downloads the embedding model (about 470 MB) and prints `ready` when everything works. Free |
| `data/05-product-pages-injected.pdf` | The help centre's product pages, as one seller edited them. The demo and Exercise 1 use it in place of the released page |

**The documents are downloaded by the notebooks**, once, and checked against
their published checksums: the help centre from Albert's Marketplace's release
`policy-corpus-v1.0.0` into `data/policy-corpus/`, and the two EU regulations
from the EU's Publications Office into `data/law/`.

**Install** (in this folder, with your lesson 1 environment active), then run
the check:

```bash
pip install -r requirements.txt
python check_setup.py
```

The lesson's setup page gives the two routes, VS Code and Google Colab, step by
step.

**In the exercise notebooks**, cells whose first line is `# GIVEN:` run as they
are. Every other code cell holds only comments: they say what to write, and you
write the code under each one. The questions you answer in words are in the
markdown cells. In `rag.py`, the same rule holds for each `STEP`.

**Cost of one full run:** the demo about $0.02, Exercise 1 about $0.03 (and
$0.02 for its optional part), Exercise 2 about $0.02. The embeddings are free:
they run on your machine.
