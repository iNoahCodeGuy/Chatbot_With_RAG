
% Noah's Portfolio Q&A (Streamlit)

An AI-powered Q&A over Noah’s professional portfolio using LangChain, OpenAI, and FAISS. The Streamlit app supports secrets-based configuration, easy index refresh, and a polished UI with optional headshot.

## Quick start (local)

1. Install deps
```bash
pip install -r requirements.txt
```

2. Set your OpenAI key (either .env or environment)
```bash
OPENAI_API_KEY=sk-...  # put this in a .env file or your shell env
```

3. Run the app
```bash
streamlit run main.py
```

4. In the sidebar, click “Create / Refresh Index” once. Then ask a question.

## Deploy on Streamlit Cloud

- App file: `main.py`
- Secrets: set `OPENAI_API_KEY` (and optionally `HEADSHOT_URL`, `HEADSHOT_NAME`)
- The app auto-builds the FAISS index on first query if missing.

## Configuration

- `OPENAI_MODEL` (default: gpt-4)
- `OPENAI_TEMPERATURE` (default: 0.1)
- `OPENAI_EMBEDDING_MODEL` (default: text-embedding-3-small)
- `CSV_FILE_PATH` (default: noah_portfolio.csv)
- `SOURCE_COLUMN` (default: answer)
- `VECTOR_DB_PATH` (default: faiss_index)
- `RETRIEVER_SCORE_THRESHOLD` (default: 0.7)

All values can be set via env or Streamlit Secrets. Secrets take precedence.

## Headshot options

Choose any one of:
- Upload in the sidebar (session-only preview)
- Set `HEADSHOT_URL` in Streamlit Secrets (preferred for Cloud)
- Add a local file under `static/noah-headshot.jpg` (or .png/.jpeg)

Optional: `HEADSHOT_NAME` in Secrets sets the caption.

## Troubleshooting

- “OpenAI key present: False” → Set `OPENAI_API_KEY` in Secrets or env.
- Embedding errors → use default `text-embedding-3-small`; verify key with “Test embedding call”.
- FAISS read error → build once via “Create / Refresh Index” or ask a question to auto-build.

## Structure

- `main.py` — Streamlit UI, diagnostics, cached QA chain
- `langchain_helper.py` — FAISS build/load and RetrievalQA chain creation
- `config.py` — Read config from Secrets/env with validation
- `requirements.txt` — dependencies
- `noah_portfolio.csv` — source data
- `faiss_index/` — persisted vector store (created at runtime)

## Note on legacy Flask files

There are legacy Flask files (`app.py`, templates/, static/js/css). The active app is Streamlit (`main.py`). You can ignore or remove Flask files if you don’t need them.