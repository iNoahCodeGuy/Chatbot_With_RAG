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
    page_title="Noah's AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper functions for special user experiences
def render_casual_visitor_experience():
    """Special experience for casual visitors with MMA highlights and contact option."""
    st.markdown("# 🎲 Welcome, Random Visitor! 👋")
    st.markdown("Since you just stumbled upon this, let me give you the fun tour of who Noah is!")
    
    # Career overview in casual tone
    st.markdown("## 🚀 Noah's Wild Career Journey")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Plot twist alert!** 📈
        
        Noah went from:
        - 💪 **Gym sales guy** (learning to persuade people)
        - 🏠 **Real estate** (bigger sales, bigger stakes)  
        - 📦 **Logistics** (keeping stuff moving)
        - ⚡ **Tesla Sales** (now we're talking tech!)
        - 🤖 **AI Engineer** (current plot: building smart assistants)
        
        Oh, and he also had **10 MMA cage fights** along the way because... why not? 🥊
        """)
    
    with col2:
        # Try to show headshot if available
        headshot_url = None
        try:
            headshot_url = st.secrets.get("HEADSHOT_URL")
        except:
            pass
        
        if headshot_url:
            st.image(headshot_url, width=200, caption="The man himself! 😄")
        else:
            st.markdown("🖼️ *[Noah's photo would go here]*")
    
    st.markdown("---")
    
    # MMA Highlights Section
    st.markdown("## 🥊 MMA Highlights - The Good Stuff!")
    st.markdown("**10 cage fights, amateur & professional. Here's the crown jewel:**")
    
    # Embed YouTube video
    st.markdown("### 🏆 Title Fight Victory")
    st.markdown("Noah defeated 5-0 fighter Edgar Sorto to win the **Fierce Fighting Championship amateur 135-lb title**!")
    
    # YouTube embed
    video_url = "https://www.youtube.com/watch?v=MgcAdEoJMzg"
    st.video(video_url)
    
    st.markdown("*Pretty cool for a guy who now codes AI assistants, right?* 😎")
    
    st.markdown("---")
    
    # Fun facts section
    st.markdown("## 🌟 Random Fun Facts")
    fun_facts = [
        "🌭 Can eat 10 hotdogs in one sitting (verified!)",
        "🧠 Got into AI after watching AlphaZero demolish Stockfish in 2017",
        "💻 Went from zero coding to building this AI assistant in months",
        "🎯 Chose Tesla as a 'bridge job' to transition from sales to tech",
        "🤖 Uses GitHub Copilot and Claude to accelerate development (smart, not lazy!)"
    ]
    
    for fact in fun_facts:
        st.markdown(f"- {fact}")
    
    st.markdown("---")
    
    # Contact section
    st.markdown("## 💬 Want to Connect with Noah?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔗 Check out his LinkedIn", use_container_width=True):
            st.link_button(
                "LinkedIn Profile", 
                "https://www.linkedin.com/in/noah-de-la-calzada-250412358/",
                use_container_width=True
            )
    
    with col2:
        if st.button("📧 Leave Noah a Message", use_container_width=True):
            render_contact_form()
    
    # Easter egg
    st.markdown("---")
    st.markdown("*P.S. This AI assistant you're using? Noah built it from scratch. Meta, right?* 🤯")

def render_crush_confession_experience():
    """Special experience for crush confessions with anonymous/open options."""
    st.markdown("# 😍 Aww, That's So Sweet! 💕")
    st.markdown("Someone has a crush on Noah! Let me help you with that... 😉")
    
    # Show Noah's attractive qualities first
    st.markdown("## ✨ What Makes Noah So Crush-Worthy?")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🔥 The Attractive Qualities:**
        - 💪 **MMA Fighter**: 10 cage fights, championship title holder
        - 🧠 **Smart Career Pivot**: Sales → AI Engineering (strategic thinker!)
        - 🚀 **Self-Driven**: Learned coding and built this AI assistant 
        - 💼 **Business Savvy**: Understands both tech and business sides
        - 🎯 **Goal-Oriented**: Clear 3-year vision, works toward it daily
        """)
    
    with col2:
        st.markdown("""
        **😊 The Personality Traits:**
        - 🤝 **Great Communicator**: Bridges technical and non-technical teams
        - 💡 **Problem Solver**: Finds creative solutions to complex challenges
        - 📈 **Growth Mindset**: Constantly learning and improving
        - 🏆 **Competitive**: But in a healthy, motivating way
        - 🌭 **Fun Side**: Can eat 10 hotdogs in one sitting (impressive!)
        """)
    
    # Headshot if available
    try:
        headshot_url = st.secrets.get("HEADSHOT_URL")
        if headshot_url:
            st.image(headshot_url, width=250, caption="The object of your affection! 😍")
    except:
        pass
    
    st.markdown("---")
    
    # Confession options
    st.markdown("## 💌 Ready to Confess?")
    st.markdown("**Would you like to confess anonymously or openly?**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🕶️ Anonymous Confession", use_container_width=True):
            st.session_state.confession_type = "anonymous"
            
    with col2:
        if st.button("😊 Open Confession", use_container_width=True):
            st.session_state.confession_type = "open"
    
    # Handle confession flow
    if "confession_type" in st.session_state:
        handle_confession_flow(st.session_state.confession_type)

def handle_confession_flow(confession_type: str):
    """Handle the confession submission flow."""
    st.markdown("---")
    
    if confession_type == "anonymous":
        st.markdown("### 🕶️ Anonymous Confession")
        st.markdown("*Your identity will remain completely private!*")
        
        confession = st.text_area(
            "Share your feelings:",
            placeholder="Tell Noah what you admire about him...",
            height=120
        )
        
        if st.button("💌 Send Anonymous Confession", disabled=not confession.strip()):
            # Store confession without identity
            store_confession(confession, anonymous=True)
            st.success("💕 Your anonymous confession has been sent to Noah!")
            st.balloons()
            
            # Option for direct message
            if st.button("📝 Leave a Direct Message Too?"):
                render_contact_form(context="confession")
                
    else:  # open confession
        st.markdown("### 😊 Open Confession")
        st.markdown("*Let Noah know who you are!*")
        
        with st.form("open_confession_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Your Name:")
            with col2:
                email = st.text_input("Your Email:")
            
            confession = st.text_area(
                "Share your feelings:",
                placeholder="Tell Noah what you admire about him and who you are...",
                height=120
            )
            
            consent = st.checkbox("I consent to sharing my contact information with Noah")
            
            submitted = st.form_submit_button("💌 Send Open Confession")
            
            if submitted:
                if not all([name.strip(), email.strip(), confession.strip()]):
                    st.error("Please fill in all fields!")
                elif not consent:
                    st.error("Please confirm your consent to share contact information.")
                else:
                    # Store confession with identity
                    store_confession(confession, anonymous=False, name=name, email=email)
                    st.success(f"💕 Your confession has been sent to Noah, {name}!")
                    st.balloons()

def store_confession(confession: str, anonymous: bool, name: str = "", email: str = ""):
    """Store confession in a simple way (could be expanded to database)."""
    import datetime
    
    # Create confessions directory if it doesn't exist
    os.makedirs("confessions", exist_ok=True)
    
    # Generate confession entry
    timestamp = datetime.datetime.now().isoformat()
    confession_data = {
        "timestamp": timestamp,
        "anonymous": anonymous,
        "confession": confession,
        "name": name if not anonymous else "Anonymous",
        "email": email if not anonymous else "Hidden"
    }
    
    # Save to file (in production, would use proper database)
    filename = f"confessions/confession_{timestamp.replace(':', '-')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"=== CONFESSION RECEIVED ===\n")
        f.write(f"Time: {timestamp}\n")
        f.write(f"Type: {'Anonymous' if anonymous else 'Open'}\n")
        if not anonymous:
            f.write(f"Name: {name}\n")
            f.write(f"Email: {email}\n")
        f.write(f"\nMessage:\n{confession}\n")

def render_contact_form(context: str = "general"):
    """Render a contact form for direct messages."""
    st.markdown("### 📧 Leave Noah a Message")
    
    with st.form("contact_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name:")
        with col2:
            email = st.text_input("Your Email:")
        
        if context == "confession":
            subject = st.text_input("Subject:", value="Following up on my confession 😊")
        else:
            subject = st.text_input("Subject:")
            
        message = st.text_area(
            "Your Message:",
            height=120,
            placeholder="What would you like to tell Noah?"
        )
        
        submitted = st.form_submit_button("📤 Send Message")
        
        if submitted:
            if not all([name.strip(), email.strip(), subject.strip(), message.strip()]):
                st.error("Please fill in all fields!")
            else:
                # Store message (similar to confession storage)
                store_message(name, email, subject, message)
                st.success(f"✅ Message sent to Noah! He'll get back to you soon.")

def store_message(name: str, email: str, subject: str, message: str):
    """Store contact message."""
    import datetime
    
    os.makedirs("messages", exist_ok=True)
    
    timestamp = datetime.datetime.now().isoformat()
    filename = f"messages/message_{timestamp.replace(':', '-')}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"=== MESSAGE RECEIVED ===\n")
        f.write(f"Time: {timestamp}\n")
        f.write(f"Name: {name}\n")
        f.write(f"Email: {email}\n")
        f.write(f"Subject: {subject}\n")
        f.write(f"\nMessage:\n{message}\n")

# Application Title
st.title("Noah's AI Assistant 🤖")

# User type selection for personalized experience
if "user_type" not in st.session_state:
    st.session_state.user_type = None

# Show greeting and user type selection if not already selected
if not st.session_state.user_type:
    st.markdown("### 👋 Hello! I'm Noah's AI Assistant")
    st.markdown("In order for me to best assist you, which best describes you?")
    
    user_types = [
        "🏢 Hiring Manager",
        "💻 Hiring Manager (Technical Background)", 
        "⚡ Software Developer",
        "🎲 Just Randomly Ended Up Here",
        "😍 Looking to Confess You Have a Crush on Noah"
    ]
    
    for user_type in user_types:
        if st.button(user_type, key=f"user_type_{user_type}", use_container_width=True):
            st.session_state.user_type = user_type
            st.rerun()
    
    st.stop()  # Don't show the rest of the interface until user type is selected

# Handle special user types with custom experiences
if st.session_state.user_type == "🎲 Just Randomly Ended Up Here":
    render_casual_visitor_experience()
    st.stop()

elif st.session_state.user_type == "😍 Looking to Confess You Have a Crush on Noah":
    render_crush_confession_experience()
    st.stop()

# Show personalized welcome message for other user types
def get_personalized_welcome(user_type: str) -> str:
    welcomes = {
        "🏢 Hiring Manager": "Perfect! I'm here to highlight Noah's business impact, leadership potential, and unique career journey. Focus on ROI, team dynamics, and measurable results.",
        "💻 Hiring Manager (Technical Background)": "Excellent! I can dive deep into Noah's technical stack, architecture decisions, and engineering approach while connecting it to business outcomes.",
        "⚡ Software Developer": "Great! Let's explore the technical implementation details, code patterns, and engineering decisions behind this AI assistant and Noah's other projects.",
    }
    return welcomes.get(user_type, "Welcome! Ask me anything about Noah.")

if st.session_state.user_type:
    st.markdown(f"### {get_personalized_welcome(st.session_state.user_type)}")

# Add reset button in sidebar for user type
with st.sidebar:
    if st.session_state.user_type:
        if st.button("🔄 Change User Type", use_container_width=True):
            st.session_state.user_type = None
            if "user_question" in st.session_state:
                del st.session_state["user_question"]
            st.rerun()

# Initialize Configuration
@st.cache_resource
def get_config() -> Config:
    """Get cached configuration instance."""
    return Config()

@st.cache_resource(show_spinner=False)
def get_qa_chain():
    """Initialize and cache the RetrievalQA chain."""
    try:
        from langchain_helper import get_qa_chain as _get
        return _get()
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
    try:
        display_name = st.secrets.get("HEADSHOT_NAME", display_name)  # type: ignore
    except Exception:
        pass
    uploaded = st.file_uploader(
        "Upload headshot (preview only)", type=["png", "jpg", "jpeg"], key="headshot_upload"
    )
    if uploaded is not None:
        st.image(uploaded, width=180, caption=display_name)
    else:
        headshot_url = None
        try:
            headshot_url = st.secrets.get("HEADSHOT_URL")  # type: ignore
        except Exception:
            pass
        if headshot_url:
            st.image(headshot_url, width=180, caption=display_name)
        else:
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
    return None

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
    st.caption("Manage the FAISS vector index powering semantic retrieval.")
    if st.button("🔄 Rebuild FAISS Index", help="Re-embed CSV and rebuild FAISS storage"):
        with st.spinner("Building FAISS index..."):
            try:
                from langchain_helper import create_vector_db
                create_vector_db()
                get_qa_chain.clear()
                st.success("✅ FAISS index rebuilt successfully")
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
    st.write("🔑 OpenAI API Key:", "✅ Present" if config.OPENAI_API_KEY else "❌ Missing")
    st.write("🤖 Embedding Model:", config.OPENAI_EMBEDDING_MODEL)
    try:
        from langchain_helper import vector_db_exists
        index_status = "✅ Ready" if vector_db_exists() else "❌ Missing"
    except Exception:
        index_status = "❌ Error"
    st.write("🗃️ FAISS Index:", index_status)
    if st.button("🧪 Test Embeddings", help="Verify OpenAI embedding functionality"):
        try:
            from langchain_helper import _get_embeddings  # type: ignore
            emb = _get_embeddings()
            vec = emb.embed_query("health check test query")
            st.success(f"✅ Embeddings OK (dim={len(vec)})")
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
                if st.button(question, key=f"popular_{i}", help=f"Asked {frequency} times"):
                    st.session_state["user_question"] = question
                    st.rerun()
        else:
            st.caption("Sample questions to get you started:")
            samples = [
                "Walk me through Noah's career so far",
                "What is Noah's professional background?",
                "List Noah's top technical skills",
                "What projects has Noah delivered?",
                "How can I connect with Noah?",
            ]
            for i, q in enumerate(samples, 1):
                if st.button(q, key=f"sample_{i}"):
                    st.session_state["user_question"] = q
                    st.rerun()
    except Exception as e:
        st.error(f"❌ Unable to load questions: {e}")

def render_environment_status():
    """Display runtime environment status (FAISS backend)."""
    try:
        import importlib
        versions = {}
        for pkg in ['langchain', 'langchain_openai', 'langchain_community', 'faiss']:  # faiss python module name varies
            try:
                mod = importlib.import_module(pkg)
                versions[pkg] = getattr(mod, '__version__', 'n/a')
            except Exception:
                pass
        ver_str = ", ".join(f"{k} {v}" for k, v in versions.items())
        st.info(f"Runtime: Vector backend FAISS | {ver_str}")
    except Exception as e:
        st.warning(f"Environment status unavailable: {e}")

# Sidebar
with st.sidebar:
    render_profile_section(config)
    render_linkedin_section(config)
    render_privacy_section()
    render_knowledge_base_section()
    render_analytics_section()
    render_popular_questions_section()
    render_diagnostics_section(config)

# Utility & Processing

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
    if analyze_question_type(question) and hasattr(config, 'LINKEDIN_URL') and config.LINKEDIN_URL:
        st.markdown("---")
        st.info("**💼 For more details about Noah's professional background:**")
        st.link_button(
            "🔗 View LinkedIn Profile",
            config.LINKEDIN_URL,
            help="Connect with Noah and view complete work history"
        )
    if sources:
        with st.expander(f"📚 Sources ({len(sources)} documents)", expanded=False):
            for i, doc in enumerate(sources, 1):
                content = getattr(doc, "page_content", "")
                preview = content[:300] + "..." if len(content) > 300 else content
                st.markdown(f"**Source {i}:** {preview}")

def process_question(question: str) -> None:
    """Process user question and generate response with full error handling."""
    try:
        from langchain_helper import vector_db_exists, create_vector_db
        if not vector_db_exists():
            with st.spinner("🔄 Building FAISS index (first-time setup)..."):
                create_vector_db()
                st.success("✅ Knowledge base ready!")
        start_time = time.time()
        # Basic retry loop for transient failures
        max_attempts = 3
        backoff_base = 1.5
        last_error = None
        for attempt in range(1, max_attempts + 1):
            try:
                with st.spinner("🤔 Generating response (attempt %d/%d)..." % (attempt, max_attempts)):
                    chain = get_qa_chain()
                    analytics = get_analytics()
                    result = chain.invoke({"query": question})
                break
            except Exception as e:
                last_error = e
                if attempt < max_attempts:
                    time.sleep(backoff_base ** attempt)
                else:
                    raise
        response_time_ms = (time.time() - start_time) * 1000
        answer = result.get("result", "I apologize, but I couldn't generate a proper response.")
        source_docs = result.get("source_documents", [])
        is_career_related = analyze_question_type(question)
        linkedin_included = (
            hasattr(config, 'LINKEDIN_URL') and config.LINKEDIN_URL and config.LINKEDIN_URL in answer
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
        render_answer_with_sources(answer, source_docs, question, config)
        st.caption(f"⚡ Response generated in {response_time_ms:.0f}ms using {len(source_docs)} sources")
    except Exception as e:
        st.error(f"❌ **Error processing question:** {str(e)}")
        st.info("💡 **Troubleshooting tips:**")
        st.write("• Check that your OpenAI API key is properly configured")
        st.write("• Try rebuilding the knowledge base using the sidebar controls")
        st.write("• Ensure your internet connection is stable")

# Main Question Interface
render_environment_status()
st.markdown("---")
st.markdown("### 💬 Ask a Question")
st.markdown("Ask anything about Noah's background, skills, experience, or projects.")
user_question = st.text_input(
    "Your question:",
    value=st.session_state.get("user_question", ""),
    placeholder="e.g., What programming languages does Noah know?",
    help="Ask about Noah's career, technical skills, projects, or background"
)
if user_question.strip():
    # Simple context length safeguard (truncate very long user inputs)
    if len(user_question) > 1200:
        st.warning("Question truncated to 1200 characters for processing safety.")
        user_question = user_question[:1200]
    if "user_question" in st.session_state:
        del st.session_state["user_question"]
    process_question(user_question.strip())






