# Noah's Portfolio Q&A (FAISS Backend)

Production-ready Streamlit RAG chatbot answering questions about Noah's background.

## Tech Stack
- Streamlit UI
- LangChain 0.3.x (invoke API)
- OpenAI GPT model + text-embedding-3-small
- FAISS vector store (single backend)
- SQLite analytics (interaction logging)

## Python Version
Pin Python to 3.11 (faiss-cpu 1.8.0.post1 not published for 3.13 yet). For Streamlit Cloud add a file `.python-version` with:
```
3.11.9
```

## Quick Start
```
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python health_check.py  # optional preflight
streamlit run main.py
```
First question builds the FAISS index from `noah_portfolio.csv`.

## Key Files
- `main.py` – UI + flow
- `langchain_helper.py` – RAG logic (FAISS only)
- `analytics.py` – logging + popular questions
- `config.py` – configuration + secrets access
- `health_check.py` – pre-deploy validation

## Rebuild Index
Use sidebar button "Rebuild FAISS Index" after updating the CSV.

## Popular Questions
Sidebar section auto-populates after a few interactions (stored in `chatbot_analytics.db`).

## Deployment (Streamlit Cloud)
1. Add secret OPENAI_API_KEY
2. Ensure `.python-version` = 3.11.x is in repo root
3. Deploy repository (main module `main.py`)
4. Ask first question (triggers index build)

## Documentation
- `DEPLOYMENT_FIX_SUMMARY.md`
- `PRODUCTION_READY_SUMMARY.md`
- `REFACTORING_SUMMARY.md`
- `ANALYTICS_GUIDE.md`
- `CONTRIBUTING.md`

## Maintenance Principles
- Keep dependencies minimal & pinned
- FAISS-only path for determinism
- Log interactions for insights; export via sidebar

---
FAISS architecture active.
