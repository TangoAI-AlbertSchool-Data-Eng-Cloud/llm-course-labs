# LLM Fundamentals: course labs

The notebooks for the LLM Fundamentals, Prompting & API Integration course
(Albert School): one folder per lesson, each with the demo the teacher runs in
class and the exercise notebooks you complete. In an exercise notebook, the
`GIVEN` cells run as they are; in every other code cell, the comments tell you
what to write.

| Folder | Lesson |
|---|---|
| `l01-tokens-and-prompting/` | How LLMs generate tokens, and how to prompt them |

## Running a notebook

1. **Python 3.12** and a virtual environment on a short path
   (`C:\llm\venv` on Windows: long paths break some packages there).
2. Install the lesson's pinned packages:
   ```bash
   pip install -r l01-tokens-and-prompting/requirements.txt
   ```
3. Put your key in a file named `.env` in the lesson's folder:
   ```text
   ANTHROPIC_API_KEY=...
   ```
   `.env` is ignored by Git. **Never commit it, never paste the key in a
   notebook cell.**
4. Open the notebook in Jupyter or VS Code and run it from the top.

**If `import anthropic` fails** with "DLL load failed" (some managed Windows
machines block compiled packages), run the notebook in Google Colab instead:
upload it, add the key under *Secrets* as `ANTHROPIC_API_KEY`, and replace the
`load_dotenv()` line with:

```python
from google.colab import userdata
import os
os.environ["ANTHROPIC_API_KEY"] = userdata.get("ANTHROPIC_API_KEY")
```

## Data

The notebooks download the company's 120 labelled support tickets from the
public release `tickets-v1.0.0` of the Albert's Marketplace repository. The
data is CC BY-SA 4.0; its card explains how it was made.
