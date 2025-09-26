# Quick Start (Option A - Chroma Only)

## 1. Prerequisites
- OpenAI API key
- Python 3.13 (Streamlit Cloud default)

## 2. Local Setup
```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...  # or set in .env
```

## 3. Run App
```
streamlit run main.py
```
First question triggers Chroma index build from `noah_portfolio.csv`.

## 4. Regenerate Index
Use sidebar button "Rebuild Index" after updating CSV.

## 5. Analytics
`chatbot_analytics.db` created automatically. Export via sidebar.

## 6. Troubleshooting
| Issue | Fix |
|-------|-----|
| Missing OpenAI key | Set OPENAI_API_KEY env or Streamlit secret |
| Chroma index not found | Ask a question or click Rebuild Index |
| Slow first response | Cold start – embeddings + index init |
| No popular questions | Ask at least 2–3 questions |

## 7. Minimal Concepts for Junior Devs
- `main.py`: UI + flow
- `langchain_helper.py`: RAG logic (Chroma only)
- `analytics.py`: SQLite logging
- `config.py`: Secrets + paths

## 8. Safe Edits
When changing prompt or retriever: adjust in `langchain_helper.py` only.

## 9. Deploy (Streamlit Cloud)
- Point app to repo root folder containing `main.py`
- Add secret OPENAI_API_KEY
- Deploy – no extra build config needed.

## 10. Next Improvements (Optional)
- Add retry/backoff wrapper (OpenAI rate limiting)
- Context chunk summarization if KB expands

---
Maintained under Option A (Chroma-only) for reliability.
