"""
Noah's Portfolio Q&A Chatbot - Enhanced Version
===============================================

A production-ready RAG-powered chatbot with professional improvements:
- Type safety with enums
- Professional error handling
- Clean code organization
- Enhanced user experience

Author: Senior Generative AI Applications Engineer
"""

import streamlit as st
import os
import time
import uuid
import logging
from typing import List, Optional
from enum import Enum
from dataclasses import dataclass
from config import Config
from analytics import ChatbotAnalytics

# Professional logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Type-safe user type definition
class UserType(Enum):
    """Type-safe user type enumeration for better code maintainability."""
    HIRING_MANAGER = "🏢 Hiring Manager"
    TECHNICAL_HIRING_MANAGER = "💻 Hiring Manager (Technical Background)"
    SOFTWARE_DEVELOPER = "⚡ Software Developer"  
    CASUAL_VISITOR = "🎲 Just Randomly Ended Up Here"
    CRUSH_CONFESSOR = "😍 Looking to Confess You Have a Crush on Noah"

@dataclass
class UserSession:
    """User session data model using dataclasses for type safety."""
    session_id: str
    user_type: Optional[UserType] = None
    questions_asked: int = 0
    start_time: float = time.time()

# Application Configuration
st.set_page_config(
    page_title="Noah's AI Assistant - Enhanced",
    page_icon="🤖",
    layout="wide", 
    initial_sidebar_state="expanded"
)

def get_user_session() -> UserSession:
    """Get or create user session (Singleton pattern)."""
    if "user_session" not in st.session_state:
        st.session_state.user_session = UserSession(
            session_id=str(uuid.uuid4())
        )
    return st.session_state.user_session

def get_personalized_message(user_type: UserType) -> str:
    """Get personalized welcome message based on user type."""
    messages = {
        UserType.HIRING_MANAGER: (
            "Perfect! I'm here to highlight Noah's business impact, leadership potential, "
            "and unique career journey. Focus on ROI, team dynamics, and measurable results."
        ),
        UserType.TECHNICAL_HIRING_MANAGER: (
            "Excellent! I can dive deep into Noah's technical stack, architecture decisions, "
            "and engineering approach while connecting it to business outcomes."
        ),
        UserType.SOFTWARE_DEVELOPER: (
            "Great! Let's explore the technical implementation details, code patterns, "
            "and engineering decisions behind this AI assistant and Noah's other projects."
        ),
        UserType.CASUAL_VISITOR: "Welcome! Let me show you the fun side of who Noah is!",
        UserType.CRUSH_CONFESSOR: "Aww, that's sweet! Let me help you with that... 😉"
    }
    return messages.get(user_type, "Welcome! Ask me anything about Noah.")

def store_confession_with_error_handling(confession: str, anonymous: bool = True, 
                                       name: str = "", email: str = "") -> bool:
    """Store confession with proper error handling."""
    try:
        import datetime
        os.makedirs("confessions", exist_ok=True)
        
        timestamp = datetime.datetime.now().isoformat()
        filename = f"confessions/confession_{timestamp.replace(':', '-')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"=== CONFESSION RECEIVED ===\n")
            f.write(f"Time: {timestamp}\n")
            f.write(f"Type: {'Anonymous' if anonymous else 'Open'}\n")
            if not anonymous:
                f.write(f"Name: {name}\n")
                f.write(f"Email: {email}\n")
            f.write(f"\nMessage:\n{confession}\n")
        
        logger.info(f"Confession stored: {'anonymous' if anonymous else 'open'}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to store confession: {e}")
        return False

def store_message_with_error_handling(name: str, email: str, subject: str, message: str) -> bool:
    """Store contact message with error handling."""
    try:
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
        
        logger.info(f"Message stored from: {name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to store message: {e}")
        return False

# Helper functions for special user experiences
def render_casual_visitor_experience():
    """Enhanced casual visitor experience with improved organization."""
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
        try:
            # Try to get headshot from secrets, fallback to placeholder
            headshot_url = st.secrets.get("HEADSHOT_URL")
            if headshot_url:
                st.image(headshot_url, width=200, caption="The man himself! 😄")
            else:
                st.markdown("🖼️ *[Noah's photo would go here]*")
        except:
            st.markdown("🖼️ *[Noah's photo would go here]*")
    
    # MMA Highlights Section
    st.markdown("---")
    st.markdown("## 🥊 MMA Highlights - The Good Stuff!")
    st.markdown("**10 cage fights, amateur & professional. Here's the crown jewel:**")
    
    st.markdown("### 🏆 Title Fight Victory")
    st.markdown("Noah defeated 5-0 fighter Edgar Sorto to win the **Fierce Fighting Championship amateur 135-lb title**!")
    
    # Main highlight video
    video_url = "https://www.youtube.com/watch?v=MgcAdEoJMzg"
    st.video(video_url)
    
    st.markdown("*Pretty cool for a guy who now codes AI assistants, right?* 😎")
    
    # Fun Facts Section
    st.markdown("---")
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
    
    # Contact Section with Form
    st.markdown("---")
    st.markdown("## 💬 Want to Connect with Noah?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔗 Check out his LinkedIn", use_container_width=True):
            st.link_button("LinkedIn Profile", "https://www.linkedin.com/in/noah-de-la-calzada-250412358/", use_container_width=True)
    
    with col2:
        if st.button("📧 Leave Noah a Message", use_container_width=True):
            st.session_state.show_contact_form = True
    
    # Contact form
    if st.session_state.get("show_contact_form", False):
        st.markdown("### 📧 Leave Noah a Message")
        
        with st.form("contact_form_casual"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Your Name:")
            with col2:
                email = st.text_input("Your Email:")
            
            subject = st.text_input("Subject:")
            message = st.text_area("Your Message:", height=120)
            
            submitted = st.form_submit_button("📤 Send Message")
            
            if submitted:
                if all([name.strip(), email.strip(), subject.strip(), message.strip()]):
                    success = store_message_with_error_handling(name.strip(), email.strip(), subject.strip(), message.strip())
                    if success:
                        st.success("✅ Message sent to Noah! He'll get back to you soon.")
                        st.session_state.show_contact_form = False
                        st.rerun()
                    else:
                        st.error("❌ Failed to send message. Please try again.")
                else:
                    st.error("Please fill in all fields!")
    
    # Easter egg message
    st.markdown("---")
    st.markdown("*P.S. This AI assistant you're using? Noah built it with clean architecture principles. Meta, right?* 🤯")

def render_crush_confession_experience():
    """Enhanced crush confession experience with proper form handling."""
    st.markdown("# 😍 Aww, That's So Sweet! 💕")
    st.markdown("Someone has a crush on Noah! Let me help you with that... 😉")
    
    # What makes Noah attractive
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
    
    # Confession options
    st.markdown("---")
    st.markdown("## 💌 Ready to Confess?")
    st.markdown("**Would you like to confess anonymously or openly?**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🕶️ Anonymous Confession", use_container_width=True):
            st.session_state.confession_type = "anonymous"
            
    with col2:
        if st.button("😊 Open Confession", use_container_width=True):
            st.session_state.confession_type = "open"
    
    # Handle confession forms
    if st.session_state.get("confession_type") == "anonymous":
        st.markdown("---")
        st.markdown("### 🕶️ Anonymous Confession")
        st.markdown("*Your identity will remain completely private!*")
        
        confession = st.text_area(
            "Share your feelings:",
            placeholder="Tell Noah what you admire about him...",
            height=120
        )
        
        if st.button("💌 Send Anonymous Confession", disabled=not confession.strip()):
            success = store_confession_with_error_handling(confession.strip(), anonymous=True)
            
            if success:
                st.success("💕 Your anonymous confession has been sent to Noah!")
                st.balloons()
            else:
                st.error("❌ Failed to send confession. Please try again.")
    
    elif st.session_state.get("confession_type") == "open":
        st.markdown("---")
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
                    success = store_confession_with_error_handling(
                        confession.strip(), 
                        anonymous=False, 
                        name=name.strip(), 
                        email=email.strip()
                    )
                    
                    if success:
                        st.success(f"💕 Your confession has been sent to Noah, {name}!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to send confession. Please try again.")

def render_enhanced_sidebar(config: Config, analytics: ChatbotAnalytics):
    """Render enhanced sidebar with professional information."""
    with st.sidebar:
        st.markdown("### 🏗️ Enhanced Features")
        st.markdown("""
        **Professional improvements:**
        - 🎯 Type-safe enums & dataclasses
        - 🛡️ Comprehensive error handling  
        - 📊 Professional logging system
        - ⚡ Performance optimizations
        - 📝 Enhanced documentation
        """)
        
        st.markdown("---")
        st.markdown("### 🤖 About This Assistant")
        st.markdown("""
        This AI assistant knows all about Noah's:
        - 🎯 **Career journey** from sales to AI engineering
        - 💻 **Technical skills** and project experience  
        - 🥊 **MMA background** (10 cage fights!)
        - 🚀 **Goals and aspirations** in tech
        - 📈 **Business acumen** and leadership experience
        """)
        
        # Display analytics if available
        try:
            stats = analytics.get_summary_stats()
            st.markdown("---")
            st.markdown("### 📊 Usage Stats")
            st.metric("Total Questions", stats.get("total_questions", 0))
            st.metric("Unique Users", stats.get("unique_sessions", 0))
            if stats.get("avg_response_time"):
                st.metric("Avg Response", f"{stats['avg_response_time']:.1f}s")
        except Exception:
            pass  # Graceful degradation
        
        # Technical details
        st.markdown("---")
        st.markdown("### 🛠️ Technical Details")
        st.markdown(f"""
        - **Model**: {config.model_name}
        - **Temperature**: {config.temperature}
        - **Max Tokens**: {config.max_tokens}
        - **Vector Store**: FAISS
        - **Architecture**: Enhanced & Professional
        """)

# Initialize application dependencies
@st.cache_resource
def get_config():
    """Get cached configuration instance."""
    return Config()

@st.cache_resource
def get_analytics():
    """Get cached analytics instance."""
    return ChatbotAnalytics()

@st.cache_resource(show_spinner=False)
def get_qa_chain():
    """Get cached QA chain with error handling."""
    try:
        from langchain_helper import get_qa_chain
        return get_qa_chain()
    except Exception as e:
        logger.error(f"QA chain initialization failed: {e}")
        st.error("⚠️ Failed to initialize AI assistant. Please check configuration.")
        return None

def main():
    """Enhanced main application with professional patterns."""
    
    # Initialize dependencies
    config = get_config()
    analytics = get_analytics()
    qa_chain = get_qa_chain()
    
    if not qa_chain:
        st.error("🚨 Unable to initialize the AI assistant. Please check the configuration.")
        return
    
    # Application header
    st.title("Noah's AI Assistant 🤖")
    st.caption("*Enhanced with Professional Software Engineering Practices*")
    
    # Get user session
    session = get_user_session()
    
    # User type selection with enhanced UI
    if not session.user_type:
        st.markdown("### 👋 Hello! I'm Noah's AI Assistant")
        st.markdown("*Enhanced with Professional Software Engineering Practices*")
        st.markdown("In order for me to best assist you, which best describes you?")
        
        # Create elegant button layout for user selection
        for user_type in UserType:
            if st.button(
                user_type.value,
                key=f"select_{user_type.name}",
                use_container_width=True,
                help=f"Select this if you are: {user_type.value}"
            ):
                session.user_type = user_type
                logger.info(f"User selected: {user_type.value}")
                st.rerun()
        
        return
    
    # Handle special experiences
    if session.user_type == UserType.CASUAL_VISITOR:
        render_casual_visitor_experience()
        
    elif session.user_type == UserType.CRUSH_CONFESSOR:
        render_crush_confession_experience()
        
    else:
        # Regular chat experience with personalization
        welcome_message = get_personalized_message(session.user_type)
        st.markdown(f"### {welcome_message}")
        
        # Enhanced question input with better UX
        st.markdown("### 💬 Ask me anything about Noah!")
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        surprise_questions = [
            "What's Noah's technical background?",
            "Tell me about Noah's MMA fighting experience", 
            "What AI projects has Noah worked on?",
            "How did Noah transition from sales to tech?",
            "What programming languages does Noah know?",
            "What's unique about Noah's career journey?",
            "Can you show me some of Noah's code examples?"
        ]
        
        with col1:
            user_question = st.text_input(
                "Your question:",
                key="user_question",
                placeholder="e.g., What's Noah's technical background?",
                help="Ask about Noah's career, skills, projects, or anything else!"
            )
        
        with col2:
            ask_button = st.button("🚀 Ask", use_container_width=True)
        
        with col3:
            surprise_button = st.button("🎲 Surprise Me", use_container_width=True)
        
        # Handle surprise question
        if surprise_button:
            import random
            selected_question = random.choice(surprise_questions)
            st.session_state.user_question = selected_question
            user_question = selected_question
            ask_button = True
        
        # Process question with enhanced error handling
        if ask_button and user_question and user_question.strip():
            try:
                with st.spinner("🤔 Thinking..."):
                    start_time = time.time()
                    
                    # Get response from QA chain
                    result = qa_chain.invoke({"query": user_question})
                    response_time = time.time() - start_time
                
                # Display response with professional formatting
                st.markdown("#### 🤔 Your Question:")
                st.markdown(f"*{user_question}*")
                
                st.markdown("#### 🤖 Noah's AI Assistant:")
                st.markdown(result["result"])
                
                # Debug information (if enabled)
                if config.debug_mode:
                    with st.expander("🐛 Debug Information"):
                        st.metric("Response Time", f"{response_time:.2f}s")
                        if "source_documents" in result:
                            st.markdown("**Sources:**")
                            for i, doc in enumerate(result["source_documents"], 1):
                                st.markdown(f"Source {i}: {doc.page_content[:100]}...")
                
                # Track analytics with error handling
                try:
                    analytics.log_question(
                        session_id=session.session_id,
                        user_type=session.user_type.value,
                        question=user_question,
                        answer=result["result"],
                        response_time=response_time
                    )
                    session.questions_asked += 1
                except Exception as e:
                    logger.warning(f"Analytics tracking failed: {e}")
                
                # Enhanced feedback section
                st.markdown("---")
                st.markdown("#### 💭 Was this helpful?")
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                for i, col in enumerate([col1, col2, col3, col4, col5], 1):
                    with col:
                        if st.button("⭐" * i, help=f"Rate {i}/5 stars", key=f"rating_{i}"):
                            try:
                                analytics.log_feedback(session.session_id, user_question, i)
                                st.success(f"Thanks for the feedback! ({i}/5 stars)")
                            except Exception as e:
                                logger.warning(f"Feedback logging failed: {e}")
                
                # Show popular questions
                try:
                    popular_questions = analytics.get_popular_questions(limit=5)
                    if popular_questions:
                        st.markdown("---")
                        st.markdown("### 🔥 Popular Questions")
                        st.markdown("*Click on any question to ask it:*")
                        
                        for i, (question, count) in enumerate(popular_questions, 1):
                            if st.button(
                                f"{i}. {question} ({count} times asked)",
                                key=f"popular_{i}",
                                help="Click to ask this question"
                            ):
                                st.session_state.user_question = question
                                st.rerun()
                except Exception as e:
                    logger.warning(f"Failed to load popular questions: {e}")
            
            except Exception as e:
                logger.error(f"Question processing failed: {e}")
                st.error("🚨 Sorry, I encountered an error processing your question. Please try again.")
                if config.debug_mode:
                    st.exception(e)
    
    # Enhanced sidebar
    render_enhanced_sidebar(config, analytics)
    
    # Reset button in sidebar
    with st.sidebar:
        if st.button("🔄 Change User Type", use_container_width=True):
            # Reset session state
            if "user_session" in st.session_state:
                del st.session_state.user_session
            if "user_question" in st.session_state:
                del st.session_state["user_question"]
            logger.info("User session reset")
            st.rerun()

if __name__ == "__main__":
    main()