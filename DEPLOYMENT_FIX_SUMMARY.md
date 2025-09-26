# Streamlit Cloud Deployment Fix Summary

## Current Target State (Modern Stack)
We are standardizing on Python 3.13 (Streamlit Cloud default) with the modern LangChain 0.3.x API (invoke pattern) and FAISS 1.12.0 (Python 3.13 wheels available). `runtime.txt` was removed because Streamlit ignores it for Python pinning and defaults to latest supported minor anyway. If FAISS wheel issues occur transiently, fallback to Chroma (`VECTOR_DB_BACKEND=chroma`).

## Original Issue (Historical)
Streamlit Cloud deployment was failing with inconsistent behavior - sometimes successfully installing updated dependencies (`faiss-cpu==1.12.0`), other times reverting to old incompatible versions (`faiss-cpu==1.8.0.post1`), indicating a cached/legacy requirements state or branch mismatch.

## Root Cause Hypotheses
1. Stale build cache referencing an earlier commit containing downgraded requirements.
2. Possible secondary requirements file during earlier iterations (now removed).
3. Transient PyPI / wheel resolution timing causing fallback attempts.
4. Branch / repository path mismatch in Streamlit app settings (case sensitivity in folder name `Chatbot_With_RAG-1`).

## Resolved Actions
- Ensured only one root-level `requirements.txt` (updated with cache-bust comment).
- Removed `runtime.txt` to avoid misleading Python pin intent.
- Confirmed modern code uses `chain.invoke()`; no legacy `.call()` / direct chain invocation remains.
- Added explicit cache-busting comment line to `requirements.txt`.
- Added FAISS→Chroma fallback logic (runtime) in `langchain_helper.py`.

## Next Deployment Steps
1. In Streamlit Cloud dashboard: confirm the repository + branch point to this folder (case-sensitive path).
2. Trigger a fresh deploy (a trivial commit already added a cache-busting comment).
3. Watch logs: you should see `faiss-cpu==1.12.0` install. If failure: set a secret `VECTOR_DB_BACKEND="chroma"` and redeploy.
4. First run will build the FAISS index (or Chroma) from `noah_portfolio.csv`.
5. Ask a couple of questions, then verify Popular Questions populate.

## Rollback (Not Recommended Now)
If you must revert temporarily to Python 3.11-era stack, you would reintroduce a `runtime.txt` specifying 3.11 and pin: `faiss-cpu==1.8.0`, `langchain==0.2.11` and revert invoke usage. This is documented only for historical traceability—current codebase expects modern versions.

## Health Check Recommendation
Add (optional) lightweight `/health` style script or a small `health_check.py` to import config, verify OpenAI key presence, and attempt an embeddings ping.

## Monitoring
Use the sidebar Diagnostics section (embedding test + index status). Analytics DB (`chatbot_analytics.db`) will appear after first logged interaction.

## Known Optional Enhancements
- Implement context length safeguard & truncation.
- Add exponential backoff wrapper for OpenAI rate limits.
- Provide CONTRIBUTING.md / QUICK_START.md for juniors.

---
Last Updated: 2025-09-26
