# Streamlit Cloud Deployment Fix Summary

## Current Target State (Option A - Chroma Only)
We standardized on Python 3.13 (Streamlit Cloud default) with the modern LangChain 0.3.x API (invoke pattern) and a **Chroma-only** vector store backend (FAISS fully removed to eliminate wheel / build variability). `runtime.txt` remains absent (Streamlit ignores it). The codebase and dependencies no longer reference FAISS; reliability > theoretical marginal speed.

## Original Issue (Historical)
Deployment instability was rooted in version drift (`faiss-cpu==1.8.0.post1` vs modern), missing packages (`langchain-openai`) and cached builds. These conditions are now structurally eliminated by:
- Removing FAISS dependency entirely
- Pinning a minimal, Python 3.13–verified requirements set
- Refactoring to a single, explicit vector backend (Chroma)

## Root Cause (Historical) Summary
1. Stale build cache + previous requirements revisions
2. Legacy FAISS version fallback due to wheel resolution timing
3. Missing `langchain-openai` caused runtime import errors
4. Multi-backend complexity increased failure surface area

## Resolved Actions
- Simplified `langchain_helper.py` to Chroma-only
- Removed all FAISS imports / conditional logic
- Updated `requirements.txt` (added `chromadb`, removed `faiss-cpu`)
- Set default `VECTOR_DB_BACKEND=chroma` in `config.py`
- Updated environment status component (no FAISS messaging)
- Added reliability-focused documentation (this file + Quick Start TBD)

## Deployment Steps (Fresh or Rebuild)
1. Push / commit any change (forces Streamlit rebuild)
2. Streamlit Cloud auto-installs minimal dependencies (watch logs for `chromadb` install)
3. First user question triggers Chroma index build from `noah_portfolio.csv`
4. Ask a few questions → verify Popular Questions populate (analytics DB appears)
5. Use Diagnostics sidebar to run Embedding Test if needed

## Health Check Script
Optional `health_check.py` (added if requested) can be run locally:
```
python health_check.py
```
It validates: OpenAI key presence, CSV load, embeddings init, Chroma create/load.

## Monitoring
- Sidebar → Analytics + Diagnostics
- `chatbot_analytics.db` created after first logged interaction
- Use Export button to snapshot usage

## Optional Enhancements (Still Open)
- Add CONTRIBUTING.md (guidelines for PRs)
- Context window guardrails (initial truncation now added in `main.py`)
- Retry / backoff wrapper (implemented) can be extended with jitter + logging
- Token-based dynamic context compression (future)

## Rollback (Not Recommended)
Reintroducing FAISS would require: adding `faiss-cpu` back to requirements, restoring multi-backend logic, and adjusting docs. Not advised unless a benchmark justifies complexity.

---
Last Updated: 2025-09-26 (Option A stabilization complete)
