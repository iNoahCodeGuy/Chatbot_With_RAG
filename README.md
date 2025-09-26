# Noah's Portfolio Q&A (Option A - Chroma Only)

Production-ready Streamlit RAG chatbot answering questions about Noah's background.

## Tech Stack
- Streamlit UI
- LangChain 0.3.x (invoke API)
- OpenAI GPT model + embeddings
- Chroma vector store (single backend for reliability)
- SQLite analytics (interaction logging)

## Quick Start
See `QUICK_START.md` for full steps.
```
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
streamlit run main.py
```
First question builds the Chroma index from `noah_portfolio.csv`.

## Key Files
- `main.py` – UI + flow
- `langchain_helper.py` – RAG logic (Chroma only)
- `analytics.py` – logging + popular questions
- `config.py` – configuration + secrets access
- `health_check.py` – pre-deploy validation

## Rebuild Index
Use sidebar button "Rebuild Index" after updating the CSV.

## Popular Questions
Sidebar section auto-populates after a few interactions (stored in `chatbot_analytics.db`).

## Deployment (Streamlit Cloud)
1. Add secret OPENAI_API_KEY
2. Deploy repository root containing `main.py`
3. Ask first question (triggers index build)

## Documentation
- `DEPLOYMENT_FIX_SUMMARY.md`
- `PRODUCTION_READY_SUMMARY.md`
- `REFACTORING_SUMMARY.md`
- `ANALYTICS_GUIDE.md`
- `CONTRIBUTING.md`

## Maintenance Principles
- Keep dependencies minimal & pinned
- Avoid reintroducing FAISS without data-driven need
- Log interactions for insights; export via sidebar

---
Built with reliability-first Option A architecture.
