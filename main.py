import streamlit as st
import os
from typing import List
from config import Config

st.set_page_config(
    page_title="Noah's Portfolio Q&A",
    page_icon="💼",
    layout="wide",
)

st.title("Noah's Portfolio Q&A 💼")

# Validate API key early with a friendly message
cfg = Config()
if not cfg.OPENAI_API_KEY:
    st.error("OpenAI API key is missing. Add it in Streamlit Secrets as OPENAI_API_KEY.")
    st.stop()

with st.sidebar:
    # --- Headshot section ---
    def _local_headshot_path() -> str | None:
        base_dir = os.path.dirname(__file__)
        for fname in ("noah-headshot.jpg", "noah-headshot.png", "noah-headshot.jpeg"):
            p = os.path.join(base_dir, "static", fname)
            if os.path.exists(p):
                return p
        return None

    display_name = "Noah"
    try:
        # Optional secret to override displayed name
        if hasattr(st, "secrets"):
            display_name = st.secrets.get("HEADSHOT_NAME", display_name)
    except Exception:
        pass

    uploaded = st.file_uploader("Upload headshot (preview only)", type=["png", "jpg", "jpeg"], key="headshot_upload")
    if uploaded is not None:
        st.image(uploaded, width=180, caption=display_name)
    else:
        # Try URL from secrets first
        url = None
        try:
            if hasattr(st, "secrets"):
                url = st.secrets.get("HEADSHOT_URL")
        except Exception:
            url = None
        if url:
            st.image(url, width=180, caption=display_name)
        else:
            local_path = _local_headshot_path()
            if local_path:
                st.image(local_path, width=180, caption=display_name)
            else:
                st.caption("Tip: add a headshot at static/noah-headshot.jpg (or .png/.jpeg) or set HEADSHOT_URL in Streamlit Secrets.")

    st.header("Knowledge Base")
    st.caption("Create or refresh the FAISS index from the portfolio CSV.")
    if st.button("🔄 Create / Refresh Index"):
        with st.spinner("Building vector index..."):
            try:
                from langchain_helper import create_vector_db
                create_vector_db()
                st.success("Index created successfully.")
            except Exception as e:
                st.error(f"Failed to create index: {e}")

    st.markdown("---")
    st.subheader("Diagnostics")
    st.caption("Quick checks to ensure the environment is configured.")
    st.write("OpenAI key present:", bool(cfg.OPENAI_API_KEY))
    st.write("Embedding model:", cfg.OPENAI_EMBEDDING_MODEL)
    try:
        from langchain_helper import vector_db_exists
        st.write("FAISS index present:", vector_db_exists())
    except Exception:
        st.write("FAISS index present:", False)
    if st.button("▶️ Test embedding call"):
        try:
            from langchain_helper import _get_embeddings  # type: ignore
            emb = _get_embeddings()
            vec = emb.embed_query("hello world")
            st.success(f"Embedding ok. Dim: {len(vec)}")
        except Exception as e:
            st.error(f"Embedding test failed: {e}")

    st.markdown("---")
    st.subheader("Sample Questions")
    samples: List[str] = [
        "What is Noah's professional background?",
        "List Noah's top technical skills.",
        "Tell me about Noah's work experience.",
        "What projects has Noah delivered?",
    ]
    for s in samples:
        if st.button(s, key=f"sample-{s[:10]}"):
            st.session_state["last_question"] = s

st.markdown("Write a question about Noah's background, skills, or projects.")
q = st.text_input(
    "Your question:",
    value=st.session_state.get("last_question", ""),
    placeholder="e.g., What programming languages does Noah know?",
)

if q:
    with st.spinner("Thinking..."):
        try:
            from langchain_helper import get_qa_chain, vector_db_exists, create_vector_db
            # Auto-build index on first use
            if not vector_db_exists():
                with st.spinner("Index not found. Building now (one-time)..."):
                    create_vector_db()
            chain = get_qa_chain()
            result = chain({"query": q})

            st.subheader("Answer")
            st.write(result.get("result", "No answer returned."))

            src_docs = result.get("source_documents") or []
            if src_docs:
                with st.expander("📚 Sources"):
                    for i, d in enumerate(src_docs, start=1):
                        content = getattr(d, "page_content", "")
                        st.write(f"Source {i}: {content[:300]}...")
        except Exception as e:
            st.error(f"Error answering question: {e}")






