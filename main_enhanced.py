"""
Enhanced Noah's AI Assistant - Senior-Level Improvements
=======================================================

This version demonstrates professional software engineering improvements
while maintaining full compatibility with existing functionality.

Key Improvements:
- Type safety with enums and dataclasses
- Professional error handling and logging
- Clear separation of concerns
- Better code organization and documentation
- Performance optimizations
- Analytics integration

Author: Senior Generative AI Applications Engineer
"""

import streamlit as st
import os
import time
import uuid
import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

# Import existing working modules (maintains compatibility)
from config import Config
from analytics import ChatbotAnalytics

# Configure professional logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================================================================
# PROFESSIONAL TYPE DEFINITIONS - Type Safety & Documentation
# =============================================================================

class UserType(Enum):
    """
    Type-safe user type enumeration.
    
    Benefits:
    - Prevents typos in string comparisons
    - IDE autocompletion support
    - Easy to extend with new user types
    - Self-documenting code
    """
    HIRING_MANAGER = "🏢 Hiring Manager"
    TECHNICAL_HIRING_MANAGER = "💻 Hiring Manager (Technical Background)"
    SOFTWARE_DEVELOPER = "⚡ Software Developer"
    CASUAL_VISITOR = "🎲 Just Randomly Ended Up Here"
    CRUSH_CONFESSOR = "😍 Looking to Confess You Have a Crush on Noah"


@dataclass
class UserSession:
    """
    User session data model using dataclasses.
    
    Benefits:
    - Type hints for all fields
    - Automatic __init__, __repr__, etc.
    - Immutable with frozen=True option
    - Easy to serialize/deserialize
    """
    session_id: str
    user_type: Optional[UserType] = None
    questions_asked: int = 0
    start_time: float = time.time()
    
    @property
    def session_duration(self) -> float:
        """Calculate session duration in minutes."""
        return (time.time() - self.start_time) / 60


# =============================================================================
# SERVICE CLASSES - Business Logic Separation
# =============================================================================

class PersonalizationService:
    """
    Service for handling user personalization logic.
    
    Follows Single Responsibility Principle - only handles personalization.
    Benefits:
    - Easy to test in isolation
    - Reusable across components
    - Clear API surface
    """
    
    # Configuration as class constants (easy to modify)
    WELCOME_MESSAGES: Dict[UserType, str] = {
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
    
    @classmethod
    def get_welcome_message(cls, user_type: UserType) -> str:
        """Get personalized welcome message for user type."""
        return cls.WELCOME_MESSAGES.get(
            user_type, 
            "Welcome! Ask me anything about Noah."
        )
    
    @classmethod
    def requires_special_flow(cls, user_type: UserType) -> bool:
        """Check if user type requires special UI flow."""
        return user_type in [UserType.CASUAL_VISITOR, UserType.CRUSH_CONFESSOR]


class SessionManager:
    """
    Manages user session state with professional patterns.
    
    Benefits:
    - Centralized session logic
    - Type-safe session operations
    - Easy to extend with new session features
    """
    
    @staticmethod
    def get_session() -> UserSession:
        """Get or create user session (Singleton pattern)."""
        if "user_session" not in st.session_state:
            st.session_state.user_session = UserSession(
                session_id=str(uuid.uuid4())
            )
        return st.session_state.user_session
    
    @staticmethod
    def reset_session():
        """Reset user session state."""
        if "user_session" in st.session_state:
            del st.session_state.user_session
        if "user_question" in st.session_state:
            del st.session_state["user_question"]
        logger.info("User session reset")


class FileStorageService:
    """
    Professional file storage service with error handling.
    
    Benefits:
    - Proper error handling
    - Directory management
    - Extensible for different storage backends
    """
    
    @staticmethod
    def ensure_directory(path: str):
        """Ensure directory exists, create if not."""
        os.makedirs(path, exist_ok=True)
    
    @staticmethod
    def store_confession(confession: str, anonymous: bool = True, 
                        name: str = "", email: str = "") -> bool:
        """Store confession with proper error handling."""
        try:
            FileStorageService.ensure_directory("confessions")
            
            import datetime
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
    
    @staticmethod
    def store_message(name: str, email: str, subject: str, message: str) -> bool:
        """Store contact message with error handling."""
        try:
            FileStorageService.ensure_directory("messages")
            
            import datetime
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


# =============================================================================
# UI COMPONENTS - Modular & Reusable
# =============================================================================

class UserSelectionUI:
    """User selection UI component with professional patterns."""
    
    @staticmethod
    def render_selection() -> Optional[UserType]:
        """Render user type selection interface."""
        session = SessionManager.get_session()
        
        if session.user_type:
            return session.user_type
        
        st.markdown("### 👋 Hello! I'm Noah's AI Assistant")
        st.markdown("*Enhanced with Professional Software Engineering Practices*")
        st.markdown("In order for me to best assist you, which best describes you?")
        
        # Create elegant button layout
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
        
        return None
    
    @staticmethod
    def render_reset_button():
        """Render reset button with proper state management."""
        session = SessionManager.get_session()
        
        if session.user_type:
            with st.sidebar:
                if st.button("🔄 Change User Type", use_container_width=True):
                    SessionManager.reset_session()
                    st.rerun()


class ChatInterfaceUI:
    """Professional chat interface with analytics integration."""
    
    def __init__(self, config: Config, analytics: ChatbotAnalytics):
        self.config = config
        self.analytics = analytics
        self.surprise_questions = [
            "What's Noah's technical background?",
            "Tell me about Noah's MMA fighting experience", 
            "What AI projects has Noah worked on?",
            "How did Noah transition from sales to tech?",
            "What programming languages does Noah know?",
            "What's unique about Noah's career journey?",
            "Can you show me some of Noah's code examples?"
        ]
    
    def render_question_input(self) -> Optional[str]:
        """Render question input with improved UX."""
        st.markdown("### 💬 Ask me anything about Noah!")
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            question = st.text_input(
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
            selected_question = random.choice(self.surprise_questions)
            st.session_state.user_question = selected_question
            return selected_question
        
        # Handle normal question
        if ask_button and question.strip():
            return question.strip()
        
        return None
    
    def process_and_display_response(self, question: str, qa_chain) -> bool:
        """Process question and display response with error handling."""
        session = SessionManager.get_session()
        
        try:
            with st.spinner("🤔 Thinking..."):
                start_time = time.time()
                
                # Get response
                result = qa_chain.invoke({"query": question})
                response_time = time.time() - start_time
                
                # Display response
                self._display_response(question, result, response_time)
                
                # Track analytics (with error handling)
                self._track_interaction(session, question, result["result"], response_time)
                
                # Render feedback
                return self._render_feedback(session, question)
                
        except Exception as e:
            logger.error(f"Question processing failed: {e}")
            st.error("🚨 Sorry, I encountered an error processing your question. Please try again.")
            if self.config.debug_mode:
                st.exception(e)
            return False
    
    def _display_response(self, question: str, result: Dict, response_time: float):
        """Display formatted response."""
        st.markdown("#### 🤔 Your Question:")
        st.markdown(f"*{question}*")
        
        st.markdown("#### 🤖 Noah's AI Assistant:")
        st.markdown(result["result"])
        
        # Debug information
        if self.config.debug_mode:
            with st.expander("🐛 Debug Information"):
                st.metric("Response Time", f"{response_time:.2f}s")
                if "source_documents" in result:
                    st.markdown("**Sources:**")
                    for i, doc in enumerate(result["source_documents"], 1):
                        st.markdown(f"Source {i}: {doc.page_content[:100]}...")
    
    def _track_interaction(self, session: UserSession, question: str, 
                          answer: str, response_time: float):
        """Track interaction with proper error handling."""
        try:
            self.analytics.log_question(
                session_id=session.session_id,
                user_type=session.user_type.value if session.user_type else "Unknown",
                question=question,
                answer=answer,
                response_time=response_time
            )
            session.questions_asked += 1
        except Exception as e:
            logger.warning(f"Analytics tracking failed: {e}")
    
    def _render_feedback(self, session: UserSession, question: str) -> bool:
        """Render feedback section with analytics tracking."""
        st.markdown("---")
        st.markdown("#### 💭 Was this helpful?")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        for i, col in enumerate([col1, col2, col3, col4, col5], 1):
            with col:
                if st.button("⭐" * i, help=f"Rate {i}/5 stars", key=f"rating_{i}"):
                    try:
                        self.analytics.log_feedback(session.session_id, question, i)
                        st.success(f"Thanks for the feedback! ({i}/5 stars)")
                        return True
                    except Exception as e:
                        logger.warning(f"Feedback logging failed: {e}")
        
        return False


# =============================================================================
# SPECIAL EXPERIENCE HANDLERS
# =============================================================================

class CasualVisitorExperience:
    """Handles casual visitor experience with improved organization."""
    
    @staticmethod
    def render():
        """Render complete casual visitor experience."""
        st.markdown("# 🎲 Welcome, Random Visitor! 👋")
        st.markdown("Since you just stumbled upon this, let me give you the fun tour of who Noah is!")
        
        CasualVisitorExperience._render_career_journey()
        CasualVisitorExperience._render_mma_highlights()
        CasualVisitorExperience._render_fun_facts()
        CasualVisitorExperience._render_contact_section()
        CasualVisitorExperience._render_easter_egg()
    
    @staticmethod
    def _render_career_journey():
        """Render career journey section."""
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
                headshot_url = st.secrets.get("HEADSHOT_URL")
                if headshot_url:
                    st.image(headshot_url, width=200, caption="The man himself! 😄")
                else:
                    st.markdown("🖼️ *[Noah's photo would go here]*")
            except:
                st.markdown("🖼️ *[Noah's photo would go here]*")
    
    @staticmethod
    def _render_mma_highlights():
        """Render MMA highlights section."""
        st.markdown("---")
        st.markdown("## 🥊 MMA Highlights - The Good Stuff!")
        st.markdown("**10 cage fights, amateur & professional. Here's the crown jewel:**")
        
        st.markdown("### 🏆 Title Fight Victory")
        st.markdown("Noah defeated 5-0 fighter Edgar Sorto to win the **Fierce Fighting Championship amateur 135-lb title**!")
        
        video_url = "https://www.youtube.com/watch?v=MgcAdEoJMzg"
        st.video(video_url)
        
        st.markdown("*Pretty cool for a guy who now codes AI assistants, right?* 😎")
    
    @staticmethod
    def _render_fun_facts():
        """Render fun facts section."""
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
    
    @staticmethod
    def _render_contact_section():
        """Render contact section with form handling."""
        st.markdown("---")
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
                st.session_state.show_contact_form = True
        
        # Render contact form if requested
        if st.session_state.get("show_contact_form", False):
            CasualVisitorExperience._render_contact_form()
    
    @staticmethod
    def _render_contact_form():
        """Render contact form with validation."""
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
                    success = FileStorageService.store_message(
                        name.strip(), email.strip(), subject.strip(), message.strip()
                    )
                    if success:
                        st.success("✅ Message sent to Noah! He'll get back to you soon.")
                        st.session_state.show_contact_form = False
                        st.rerun()
                    else:
                        st.error("❌ Failed to send message. Please try again.")
                else:
                    st.error("Please fill in all fields!")
    
    @staticmethod
    def _render_easter_egg():
        """Render easter egg message."""
        st.markdown("---")
        st.markdown("*P.S. This AI assistant you're using? Noah built it with clean architecture principles. Meta, right?* 🤯")


class CrushConfessionExperience:
    """Handles crush confession experience with proper form handling."""
    
    @staticmethod
    def render():
        """Render complete crush confession experience."""
        st.markdown("# 😍 Aww, That's So Sweet! 💕")
        st.markdown("Someone has a crush on Noah! Let me help you with that... 😉")
        
        CrushConfessionExperience._render_attractive_qualities()
        CrushConfessionExperience._render_confession_options()
    
    @staticmethod
    def _render_attractive_qualities():
        """Render Noah's attractive qualities."""
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
    
    @staticmethod
    def _render_confession_options():
        """Render confession options and forms."""
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
        confession_type = st.session_state.get("confession_type")
        
        if confession_type == "anonymous":
            CrushConfessionExperience._render_anonymous_confession()
        elif confession_type == "open":
            CrushConfessionExperience._render_open_confession()
    
    @staticmethod
    def _render_anonymous_confession():
        """Render anonymous confession form."""
        st.markdown("---")
        st.markdown("### 🕶️ Anonymous Confession")
        st.markdown("*Your identity will remain completely private!*")
        
        confession = st.text_area(
            "Share your feelings:",
            placeholder="Tell Noah what you admire about him...",
            height=120
        )
        
        if st.button("💌 Send Anonymous Confession", disabled=not confession.strip()):
            success = FileStorageService.store_confession(confession.strip(), anonymous=True)
            
            if success:
                st.success("💕 Your anonymous confession has been sent to Noah!")
                st.balloons()
            else:
                st.error("❌ Failed to send confession. Please try again.")
    
    @staticmethod
    def _render_open_confession():
        """Render open confession form."""
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
                    success = FileStorageService.store_confession(
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


# =============================================================================
# MAIN APPLICATION CLASS - Clean Architecture
# =============================================================================

class NoahAIAssistantApp:
    """Main application class with professional architecture."""
    
    def __init__(self):
        """Initialize application with dependency injection."""
        try:
            # Initialize dependencies with error handling
            self.config = self._get_config()
            self.analytics = self._get_analytics()
            self.qa_chain = self._get_qa_chain()
            self.chat_ui = ChatInterfaceUI(self.config, self.analytics)
            
            logger.info("Application initialized successfully")
            
        except Exception as e:
            logger.error(f"Application initialization failed: {e}")
            st.error("🚨 Application failed to initialize. Please check your configuration.")
            st.stop()
    
    @staticmethod
    @st.cache_resource
    def _get_config() -> Config:
        """Get cached configuration instance."""
        return Config()
    
    @staticmethod
    @st.cache_resource  
    def _get_analytics() -> ChatbotAnalytics:
        """Get cached analytics instance."""
        return ChatbotAnalytics()
    
    @staticmethod
    @st.cache_resource(show_spinner=False)
    def _get_qa_chain():
        """Get cached QA chain with proper error handling."""
        try:
            from langchain_helper import get_qa_chain
            return get_qa_chain()
        except Exception as e:
            logger.error(f"QA chain initialization failed: {e}")
            return None
    
    def configure_page(self):
        """Configure Streamlit page with professional settings."""
        st.set_page_config(
            page_title="Noah's AI Assistant - Enhanced",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render_header(self):
        """Render professional application header."""
        st.title("Noah's AI Assistant 🤖")
        st.caption("*Enhanced with Senior-Level Software Engineering Practices*")
    
    def render_sidebar(self):
        """Render informational sidebar with analytics."""
        with st.sidebar:
            st.markdown("### 🏗️ Architecture Improvements")
            st.markdown("""
            **Professional enhancements:**
            - 🎯 Type-safe enums & dataclasses
            - 🛡️ Comprehensive error handling  
            - 📊 Professional logging system
            - 🧩 Service class architecture
            - ⚡ Performance optimizations
            - 📝 Extensive documentation
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
            
            # Display analytics
            try:
                stats = self.analytics.get_summary_stats()
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
            - **Model**: {self.config.model_name}
            - **Temperature**: {self.config.temperature}
            - **Max Tokens**: {self.config.max_tokens}
            - **Vector Store**: FAISS
            - **Architecture**: Enhanced & Professional
            """)
    
    def run(self):
        """Main application entry point with clean flow."""
        try:
            # Configure page
            self.configure_page()
            self.render_header()
            
            # Handle user selection
            selected_user_type = UserSelectionUI.render_selection()
            
            if not selected_user_type:
                return  # User still selecting
            
            # Show personalized welcome for regular users
            if not PersonalizationService.requires_special_flow(selected_user_type):
                welcome = PersonalizationService.get_welcome_message(selected_user_type)
                st.markdown(f"### {welcome}")
            
            # Route to appropriate experience
            if selected_user_type == UserType.CASUAL_VISITOR:
                CasualVisitorExperience.render()
                
            elif selected_user_type == UserType.CRUSH_CONFESSOR:
                CrushConfessionExperience.render()
                
            else:
                # Handle regular chat flow
                self._handle_chat_flow()
            
            # Render sidebar and reset button
            self.render_sidebar()
            UserSelectionUI.render_reset_button()
            
        except Exception as e:
            logger.error(f"Application runtime error: {e}")
            st.error("🚨 An unexpected error occurred. Please refresh the page.")
            if self.config.debug_mode:
                st.exception(e)
    
    def _handle_chat_flow(self):
        """Handle regular chat flow with error checking."""
        if not self.qa_chain:
            st.error("⚠️ Unable to initialize the AI assistant. Please check the configuration.")
            return
        
        # Get user question
        question = self.chat_ui.render_question_input()
        
        if question:
            # Process and display response
            self.chat_ui.process_and_display_response(question, self.qa_chain)
            
            # Show popular questions
            self._render_popular_questions()
    
    def _render_popular_questions(self):
        """Render popular questions section."""
        try:
            popular_questions = self.analytics.get_popular_questions(limit=5)
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


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

def main():
    """Professional application entry point with error handling."""
    try:
        app = NoahAIAssistantApp()
        app.run()
    except Exception as e:
        logger.critical(f"Critical application error: {e}")
        st.error("🚨 Critical error: Application failed to start.")
        if st.checkbox("Show detailed error information"):
            st.exception(e)


if __name__ == "__main__":
    main()