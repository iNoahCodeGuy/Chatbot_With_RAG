# Contributing Guide

## Branching
- main = production
- feature/* = new work
- docs/* = documentation only

## Workflow
1. Create issue or reference existing one
2. Create feature branch
3. Make focused commits (present tense)
4. Run local smoke test:
   - `streamlit run main.py`
   - Ask a question, verify answer + sources
5. Run `python final_validation.py` (add tests here as project grows)
6. Open PR → concise description + screenshots if UI changes

## Code Style
- Prefer clarity over cleverness
- Add docstrings for new public functions
- Keep functions < 60 lines when practical
- Use type hints

## RAG Specific
- Modify retriever/prompt only in `langchain_helper.py`
- Do not introduce FAISS unless justified with benchmark
- Keep Chroma index path configurable via env if changed

## Dependencies
- Pin exact versions in `requirements.txt`
- Avoid adding heavy libs unless essential

## Secrets
Never commit secrets. Use environment variables or `.streamlit/secrets.toml` (gitignored).

## Analytics
If schema changes: add migration snippet in PR description.

## Testing Ideas (Future)
- Add unit tests for analytics aggregation
- Add mock tests for prompt assembly
- Add latency budget alerts

## Release
- Squash merge small feature branches
- Tag versions if introducing breaking changes

---
Thank you for contributing! Keep it reliable, simple, and well-documented.
