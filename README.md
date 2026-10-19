# LLM Fundamentals: course labs

The notebooks for the LLM Fundamentals, Prompting & API Integration course
(Albert School): one folder per lesson, each with the demo the teacher runs in
class and the exercise notebooks you complete. In an exercise notebook, the
`GIVEN` cells run as they are; in every other code cell, the comments tell you
what to write.

| Folder | Lesson |
|---|---|
| `l01-tokens-and-prompting/` | How LLMs generate tokens, and how to prompt them |
| `l02-api-and-structured-output/` | Programmatic API use and structured outputs |
| `l03-rag/` | Retrieval-augmented generation |

## Running a notebook

1. **Python 3.12** and a virtual environment on a short path
   (`C:\llm\venv` on Windows: long paths break some packages there).
2. Install the lesson's pinned packages:
   ```bash
   pip install -r l01-tokens-and-prompting/requirements.txt
   ```
3. Put your key in a file named `.env` in the lesson's folder. With an
   Anthropic key (`sk-ant-…`):
   ```text
   ANTHROPIC_API_KEY=...
   ```
   With an OpenRouter key (`sk-or-…`), these two lines instead, and no
   `ANTHROPIC_API_KEY` line:
   ```text
   ANTHROPIC_BASE_URL=https://openrouter.ai/api
   ANTHROPIC_AUTH_TOKEN=...
   ```
   The code is the same for both. `.env` is ignored by Git. **Never commit it, never paste the key in a
   notebook cell.**
4. Open the notebook in Jupyter or VS Code and run it from the top.

**If `import anthropic` fails** with "DLL load failed" (some managed Windows
machines block compiled packages), run the notebook in Google Colab instead:
upload it, add the key under *Secrets* as `ANTHROPIC_API_KEY` (an Anthropic
key) or `OPENROUTER_API_KEY` (an OpenRouter key), with notebook access on, then
uncomment the notebook's first code cell and run it before any other.

## Data

The notebooks download the company's 120 labelled support tickets from the
public release `tickets-v1.0.0` of the Albert's Marketplace repository. The
data is CC BY-SA 4.0; its card explains how it was made.
