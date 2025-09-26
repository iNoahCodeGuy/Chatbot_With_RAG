import streamlit as st
import os
import time
from typing import List
from config import Config
from analytics import ChatbotAnalytics

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

@st.cache_resource(show_spinner=False)
def _get_cached_chain():
    """Cache the RetrievalQA chain across reruns for responsiveness."""
    from langchain_helper import get_qa_chain
    return get_qa_chain()

@st.cache_resource(show_spinner=False)
def _get_cached_analytics():
    """Cache the analytics instance across reruns."""
    return ChatbotAnalytics()

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

    # LinkedIn Profile button
    linkedin_url = cfg.LINKEDIN_URL if hasattr(cfg, 'LINKEDIN_URL') else ""
    if linkedin_url:
        st.markdown("---")
        st.link_button("🔗 LinkedIn Profile", linkedin_url, help="View Noah's professional background", use_container_width=True)

    # --- Privacy & How it works ---
    st.markdown("---")
    st.subheader("🔒 Privacy & How it works")
    st.caption(
        "- Your queries go to OpenAI for processing.\n"
        "- No chat history is sent to third-party analytics.\n"
        "- Minimal local analytics stored in SQLite (chatbot_analytics.db).\n"
        "- Sources for answers are shown for transparency."
    )

    st.header("Knowledge Base")
    st.caption("Create or refresh the FAISS index from the portfolio CSV.")
    if st.button("🔄 Create / Refresh Index"):
        with st.spinner("Building vector index..."):
            try:
                from langchain_helper import create_vector_db
                create_vector_db()
                # Clear cached chain so it reloads the updated index
                _get_cached_chain.clear()
                st.success("Index created successfully.")
            except Exception as e:
                st.error(f"Failed to create index: {e}")

    st.markdown("---")
    st.subheader("📊 Analytics")
    try:
        analytics = _get_cached_analytics()
        stats = analytics.get_analytics_summary()
        
        total = stats.get('total_interactions', 0)
        if total > 0:
            st.metric("Total Questions", total)
            
            col1, col2 = st.columns(2)
            with col1:
                career_pct = (stats.get('career_questions', 0) / total) * 100
                st.metric("Career Q's", f"{career_pct:.0f}%")
            with col2:
                # Use correct key from analytics summary
                avg_ms = stats.get('avg_response_time_ms', 0) or 0
                st.metric("Avg Time", f"{avg_ms:.0f}ms")
            
            if st.button("📈 Export Analytics"):
                # Provide an explicit export path; show row count on success
                export_path = f"analytics_export_{int(time.time())}.csv"
                try:
                    rows = analytics.export_data(export_path)
                    st.success(f"Exported {rows} rows to {export_path}")
                except Exception as e:
                    st.error(f"Export failed: {e}")
        else:
            st.info("No interactions logged yet")
            
    except Exception as e:
        st.error(f"Analytics error: {e}")

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
        "Walk me through Noah's career so far",
        "What is Noah's professional background?",
        "List Noah's top technical skills",
        "What projects has Noah delivered?",
        "How can I connect with Noah?",
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
            from langchain_helper import vector_db_exists, create_vector_db
            # Auto-build index on first use
            if not vector_db_exists():
                with st.spinner("Index not found. Building now (one-time)..."):
                    create_vector_db()
            
            # Start timing the response
            start_time = time.time()
            chain = _get_cached_chain()
            analytics = _get_cached_analytics()
            result = chain({"query": q})
            response_time_ms = (time.time() - start_time) * 1000
            
            answer = result.get("result", "No answer returned.")
            src_docs = result.get("source_documents") or []

            # Check if this is a career-related question and show LinkedIn button
            career_keywords = ["career", "background", "experience", "work", "job", "role", "linkedin", "connect", "history", "resume", "cv"]
            is_career_related = any(keyword in q.lower() for keyword in career_keywords)
            linkedin_included = cfg.LINKEDIN_URL in answer if hasattr(cfg, 'LINKEDIN_URL') and cfg.LINKEDIN_URL else False

            # Log the interaction to analytics
            session_id = st.session_state.get('session_id')
            if not session_id:
                import uuid
                session_id = str(uuid.uuid4())[:8]
                st.session_state['session_id'] = session_id

            analytics.log_interaction(
                question=q,
                answer=answer,
                source_count=len(src_docs),
                response_time_ms=response_time_ms,
                linkedin_included=linkedin_included,
                is_career_related=is_career_related,
                session_id=session_id
            )

            st.subheader("Answer")
            st.write(answer)

            if is_career_related:
                linkedin_url = cfg.LINKEDIN_URL if hasattr(cfg, 'LINKEDIN_URL') else ""
                if linkedin_url:
                    st.markdown("---")
                    st.markdown("**📋 View Noah's complete professional profile:**")
                    st.link_button("🔗 Open LinkedIn Profile", linkedin_url, help="View Noah's full work history and connect on LinkedIn")

            if src_docs:
                with st.expander("📚 Sources"):
                    for i, d in enumerate(src_docs, start=1):
                        content = getattr(d, "page_content", "")
                        st.write(f"Source {i}: {content[:300]}...")
        except Exception as e:
            st.error(f"Error answering question: {e}")






