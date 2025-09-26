"""
Noah's Portfolio Q&A Chatbot
============================

A production-ready RAG-powered chatbot for answering questions about Noah's 
professional background, built with LangChain, OpenAI, and Streamlit.

Author: Senior Generative AI Applications Engineer
"""

import streamlit as st
import os
import time
import uuid
from typing import List, Optional
from config import Config
from analytics import ChatbotAnalytics

# Application Configuration
st.set_page_config(
    page_title="Noah's Portfolio Q&A",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Application Title
st.title("Noah's Portfolio Q&A 💼")

# Initialize Configuration
@st.cache_resource
def get_config() -> Config:
    """Get cached configuration instance."""
    return Config()

@st.cache_resource(show_spinner=False)
def get_qa_chain():
    """Initialize and cache the RetrievalQA chain."""
    try:
        from langchain_helper import get_qa_chain
        return get_qa_chain()
    except Exception as e:
        st.error(f"Failed to initialize Q&A system: {e}")
        st.stop()

@st.cache_resource(show_spinner=False)
def get_analytics() -> ChatbotAnalytics:
    """Initialize and cache the analytics system."""
    return ChatbotAnalytics()

# Validate Configuration Early
config = get_config()
if not config.OPENAI_API_KEY:
    st.error("🔑 OpenAI API key is required. Please add OPENAI_API_KEY to Streamlit Secrets.")
    st.stop()

def render_profile_section(config: Config) -> None:
    """Render the profile section with headshot and LinkedIn integration."""
    display_name = "Noah"
    
    # Try to get custom name from secrets
    try:
        display_name = st.secrets.get("HEADSHOT_NAME", display_name)
    except Exception:
        pass

    # Handle headshot upload (development feature)
    uploaded = st.file_uploader(
        "Upload headshot (preview only)", 
        type=["png", "jpg", "jpeg"], 
        key="headshot_upload"
    )
    
    if uploaded is not None:
        st.image(uploaded, width=180, caption=display_name)
    else:
        # Try headshot URL from secrets
        headshot_url = None
        try:
            headshot_url = st.secrets.get("HEADSHOT_URL")
        except Exception:
            pass
            
        if headshot_url:
            st.image(headshot_url, width=180, caption=display_name)
        else:
            # Try local headshot file
            local_headshot = _find_local_headshot()
            if local_headshot:
                st.image(local_headshot, width=180, caption=display_name)
            else:
                st.caption("💡 Tip: Add HEADSHOT_URL to Streamlit Secrets or place noah-headshot.jpg in static/")

def _find_local_headshot() -> Optional[str]:
    """Find local headshot file in static directory."""
    base_dir = os.path.dirname(__file__)
    for filename in ("noah-headshot.jpg", "noah-headshot.png", "noah-headshot.jpeg"):
        path = os.path.join(base_dir, "static", filename)
        if os.path.exists(path):
            return path
def render_linkedin_section(config: Config) -> None:
    """Render LinkedIn profile integration."""
    if hasattr(config, 'LINKEDIN_URL') and config.LINKEDIN_URL:
        st.markdown("---")
        st.link_button(
            "🔗 LinkedIn Profile", 
            config.LINKEDIN_URL, 
            help="View Noah's professional background",
            use_container_width=True
        )

def render_privacy_section() -> None:
    """Render privacy and how it works information."""
    st.markdown("---")
    st.subheader("🔒 Privacy & Security")
    st.caption(
        "• **OpenAI Processing**: Questions sent to OpenAI for AI responses\n"
        "• **No Data Sharing**: Chat history never shared with third parties\n"
        "• **Local Analytics**: Minimal usage stats stored locally (SQLite)\n"
        "• **Source Transparency**: All answers include verifiable sources"
    )

def render_knowledge_base_section() -> None:
    """Render knowledge base management controls."""
    st.header("Knowledge Base")
    st.caption("Manage the vector database that powers intelligent responses.")
    
    if st.button("🔄 Rebuild Index", help="Refresh the vector database from portfolio data"):
        with st.spinner("Building vector index..."):
            try:
                from langchain_helper import create_vector_db
                create_vector_db()
                # Clear cached resources
                get_qa_chain.clear()
                st.success("✅ Vector index rebuilt successfully")
            except Exception as e:
                st.error(f"❌ Failed to rebuild index: {e}")

def render_analytics_section() -> None:
    """Render analytics dashboard in sidebar."""
    st.markdown("---")
    st.subheader("📊 Analytics Dashboard")
    
    try:
        analytics = get_analytics()
        stats = analytics.get_analytics_summary()
        
        total = stats.get('total_interactions', 0)
        if total > 0:
            st.metric("Total Questions", total)
            
            col1, col2 = st.columns(2)
            with col1:
                career_pct = (stats.get('career_questions', 0) / total) * 100
                st.metric("Career Focus", f"{career_pct:.0f}%")
            with col2:
                avg_ms = stats.get('avg_response_time_ms', 0) or 0
                st.metric("Avg Response", f"{avg_ms:.0f}ms")
            
            if st.button("📈 Export Data", help="Export analytics to CSV file"):
                export_path = f"analytics_export_{int(time.time())}.csv"
                try:
                    rows = analytics.export_data(export_path)
                    st.success(f"✅ Exported {rows} interactions to {export_path}")
                except Exception as e:
                    st.error(f"❌ Export failed: {e}")
        else:
            st.info("📊 No analytics data available yet")
            
    except Exception as e:
        st.error(f"❌ Analytics system error: {e}")

def render_diagnostics_section(config: Config) -> None:
    """Render system diagnostics for debugging."""
    st.markdown("---")
    st.subheader("🔧 System Diagnostics")
    
    # Configuration status
    st.write("🔑 OpenAI API Key:", "✅ Present" if config.OPENAI_API_KEY else "❌ Missing")
    st.write("🤖 AI Model:", config.OPENAI_EMBEDDING_MODEL)
    
    # Vector database status
    try:
        from langchain_helper import vector_db_exists
        index_status = "✅ Ready" if vector_db_exists() else "❌ Missing"
    except Exception:
        index_status = "❌ Error"
    st.write("🗃️ Vector Index:", index_status)
    
    # Test embedding functionality
    if st.button("🧪 Test Embeddings", help="Verify OpenAI embedding functionality"):
        try:
            from langchain_helper import _get_embeddings
            embeddings = _get_embeddings()
            test_vector = embeddings.embed_query("test query")
            st.success(f"✅ Embeddings working (dimension: {len(test_vector)})")
        except Exception as e:
            st.error(f"❌ Embedding test failed: {e}")

def render_popular_questions_section() -> None:
    """Render popular questions with fallback to samples."""
    st.markdown("---")
    st.subheader("💡 Popular Questions")
    
    try:
        analytics = get_analytics()
        popular = analytics.get_popular_questions(limit=5, days=30)
        
        if popular:
            st.caption("Most asked questions (last 30 days):")
            for i, item in enumerate(popular, 1):
                question = item['question']
                frequency = item['frequency']
                if st.button(
                    f"{question}", 
                    key=f"popular_{i}",
                    help=f"Asked {frequency} times"
                ):
                    st.session_state["user_question"] = question
                    st.rerun()
        else:
            # Fallback to curated sample questions
            st.caption("Sample questions to get you started:")
            sample_questions = [
                "Walk me through Noah's career so far",
                "What is Noah's professional background?", 
                "List Noah's top technical skills",
                "What projects has Noah delivered?",
                "How can I connect with Noah?"
            ]
            
            for i, question in enumerate(sample_questions, 1):
                if st.button(question, key=f"sample_{i}"):
                    st.session_state["user_question"] = question
                    st.rerun()
                    
    except Exception as e:
        st.error(f"❌ Unable to load questions: {e}")

# Render Sidebar
with st.sidebar:
    render_profile_section(config)
    render_linkedin_section(config)
    render_privacy_section()
    render_knowledge_base_section()
    render_analytics_section()
    render_popular_questions_section()
    render_diagnostics_section(config)

    st.markdown("---")
    st.subheader("Popular Questions")
    try:
        analytics = get_analytics()
        popular = analytics.get_popular_questions(limit=5, days=30)
        
        if popular:
            st.caption("Most asked questions in the last 30 days:")
            for i, item in enumerate(popular, 1):
                question = item['question']
                frequency = item['frequency']
                if st.button(f"{question} ({frequency}×)", key=f"popular-{i}", help=f"Asked {frequency} times"):
                    st.session_state["last_question"] = question
        else:
            # Fallback to sample questions if no popular data yet
            st.caption("Sample questions to get you started:")
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
    except Exception as e:
        # Fallback to sample questions on error
        st.caption("Sample questions to get you started:")
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

def get_session_id() -> str:
    """Get or create a unique session ID for analytics tracking."""
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = str(uuid.uuid4())[:8]
    return st.session_state['session_id']

def analyze_question_type(question: str) -> bool:
    """Determine if a question is career-related based on keywords."""
    career_keywords = [
        "career", "background", "experience", "work", "job", "role", 
        "linkedin", "connect", "history", "resume", "cv", "professional"
    ]
    return any(keyword in question.lower() for keyword in career_keywords)

def render_answer_with_sources(answer: str, sources: List, question: str, config: Config) -> None:
    """Render the AI answer with professional formatting and source attribution."""
    st.subheader("💡 Answer")
    st.write(answer)
    
    # Show LinkedIn integration for career questions
    if analyze_question_type(question) and hasattr(config, 'LINKEDIN_URL') and config.LINKEDIN_URL:
        st.markdown("---")
        st.info("**💼 For more details about Noah's professional background:**")
        st.link_button(
            "🔗 View LinkedIn Profile", 
            config.LINKEDIN_URL, 
            help="Connect with Noah and view complete work history"
        )
    
    # Show source documents
    if sources:
        with st.expander(f"📚 Sources ({len(sources)} documents)", expanded=False):
            for i, doc in enumerate(sources, 1):
                content = getattr(doc, "page_content", "")
                preview = content[:300] + "..." if len(content) > 300 else content
                st.markdown(f"**Source {i}:** {preview}")

def process_question(question: str) -> None:
    """Process user question and generate response with full error handling."""
    try:
        # Ensure vector database exists
        from langchain_helper import vector_db_exists, create_vector_db
        
        if not vector_db_exists():
            with st.spinner("🔄 Building knowledge base (first-time setup)..."):
                create_vector_db()
                st.success("✅ Knowledge base ready!")
        
        # Generate response with timing
        start_time = time.time()
        
        with st.spinner("🤔 Analyzing question and generating response..."):
            chain = get_qa_chain()
            analytics = get_analytics()
            
            result = chain.invoke({"query": question})
            response_time_ms = (time.time() - start_time) * 1000
            
            answer = result.get("result", "I apologize, but I couldn't generate a proper response.")
            source_docs = result.get("source_documents", [])
            
            # Analytics tracking
            is_career_related = analyze_question_type(question)
            linkedin_included = (
                hasattr(config, 'LINKEDIN_URL') and 
                config.LINKEDIN_URL and 
                config.LINKEDIN_URL in answer
            )
            
            analytics.log_interaction(
                question=question,
                answer=answer,
                source_count=len(source_docs),
                response_time_ms=response_time_ms,
                linkedin_included=linkedin_included,
                is_career_related=is_career_related,
                session_id=get_session_id()
            )
            
            # Render results
            render_answer_with_sources(answer, source_docs, question, config)
            
            # Show performance metrics
            st.caption(f"⚡ Response generated in {response_time_ms:.0f}ms using {len(source_docs)} sources")
            
    except Exception as e:
        st.error(f"❌ **Error processing question:** {str(e)}")
        st.info("💡 **Troubleshooting tips:**")
        st.write("• Check that your OpenAI API key is properly configured")
        st.write("• Try rebuilding the knowledge base using the sidebar controls")
        st.write("• Ensure your internet connection is stable")

# Main Question Interface
st.markdown("---")
st.markdown("### 💬 Ask a Question")
st.markdown("Ask anything about Noah's background, skills, experience, or projects.")

# Get user input
user_question = st.text_input(
    "Your question:",
    value=st.session_state.get("user_question", ""),
    placeholder="e.g., What programming languages does Noah know?",
    help="Ask about Noah's career, technical skills, projects, or background"
)

# Process question if provided
if user_question.strip():
    # Clear the session state to avoid re-triggering
    if "user_question" in st.session_state:
        del st.session_state["user_question"]
    
    process_question(user_question.strip())






