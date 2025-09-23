import streamlit as st
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
            from langchain_helper import get_qa_chain
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






