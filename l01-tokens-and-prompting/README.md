# Lesson 1: tokens and prompting

| File | What it is |
|---|---|
| `demo.ipynb` | The demo, with the outputs it printed when the teacher ran it. Run it again and compare: your numbers will differ |
| `exercise-1.ipynb` | Exercise 1, in class, in pairs: route the tickets with three prompt patterns |
| `exercise-2.ipynb` | Exercise 2, at home: where the eight labels fail |
| `requirements.txt` | The packages, pinned to the versions the demo ran with |
| `check_setup.py` | Run once before session 1: prints `ready` when Python, the packages and the key all work. Free |
| `data/t020_translations.json` | Ticket T020 in English, and translated into French and German by a model for the token-count comparison. Test material, not data |

**In the exercise notebooks**, cells whose first line is `# GIVEN:` run as
they are. Every other code cell holds only comments: they say what to write,
and you write the code under each one. The questions you answer in words are
in the markdown cells, right where they come up.

The tickets themselves are downloaded by the first cells into
`data/tickets_v1.csv` (ignored by Git).

**Cost of one full run of the demo:** about $0.25, most of it in the cells that
call Claude Opus 5.5. Skip those when replaying and it is about $0.05.
