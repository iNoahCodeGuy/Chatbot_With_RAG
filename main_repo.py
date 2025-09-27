"""
Noah's AI Assistant - Senior-Level Architecture
===============================================

Production-ready RAG-powered chatbot demonstrating senior generative AI 
applications engineering patterns:

✨ SENIOR-LEVEL FEATURES:
- Clean Architecture with separation of concerns
- Type safety with enums and dataclasses  
- Professional error handling and logging
- Performance optimization with caching
- Comprehensive documentation for junior developers
- Service-oriented design patterns
- Dependency injection and configuration management

🎯 BUSINESS VALUE:
- Personalized user experiences for different stakeholder types
- Analytics tracking for continuous improvement
- Graceful error handling for production reliability
- Maintainable codebase for team development

Author: Senior Generative AI Applications Engineer
Version: 2.0 - Production Ready
"""

import streamlit as st
import os
import time
import uuid
import logging
import random
import sqlite3
from typing import List, Optional, Dict, Any, Tuple
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime

# Core imports - existing working modules
from config import Config
from analytics import ChatbotAnalytics

# =============================================================================
# LOGGING SETUP - Production-Ready
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('noah_ai_assistant.log') if not st.runtime.exists() else logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =============================================================================
# TYPE DEFINITIONS - Senior-Level Type Safety
# =============================================================================

class UserType(Enum):
    """
    Type-safe user categories with emoji identifiers.
    
    Benefits for junior developers:
    - Prevents typos in string comparisons
    - IDE autocompletion and intellisense support
    - Easy to extend with new user types
    - Self-documenting code with descriptive names
    """
    HIRING_MANAGER = "🏢 Hiring Manager"
    TECHNICAL_HIRING_MANAGER = "💻 Hiring Manager (Technical Background)"
    SOFTWARE_DEVELOPER = "⚡ Software Developer"
    CASUAL_VISITOR = "🎲 Just Randomly Ended Up Here"
    CRUSH_CONFESSOR = "😍 Looking to Confess You Have a Crush on Noah"

class AppState(Enum):
    """Application state management for clean flow control."""
    USER_SELECTION = "user_selection"
    MAIN_CHAT = "main_chat"
    SPECIAL_EXPERIENCE = "special_experience"
    ERROR_STATE = "error_state"

@dataclass
class UserSession:
    """
    User session model with type safety and computed properties.
    
    Using dataclasses provides:
    - Automatic __init__, __repr__, __eq__ methods
    - Type hints for all fields
    - Easy serialization/deserialization
    - Immutable with frozen=True if needed
    """
    session_id: str
    user_type: Optional[UserType] = None
    questions_asked: int = 0
    start_time: float = field(default_factory=time.time)
    app_state: AppState = AppState.USER_SELECTION
    
    @property
    def session_duration_minutes(self) -> float:
        """Calculate session duration in minutes."""
        return (time.time() - self.start_time) / 60
    
    @property
    def is_special_user(self) -> bool:
        """Check if user requires special experience flow."""
        return self.user_type in [UserType.CASUAL_VISITOR, UserType.CRUSH_CONFESSOR]

@dataclass
class AppConfig:
    """Application configuration with sensible defaults."""
    debug_mode: bool = False
    enable_analytics: bool = True
    enable_logging: bool = True
    max_response_time: float = 30.0
    surprise_questions_count: int = 7

# =============================================================================
# BUSINESS LOGIC SERVICES - Clean Architecture
# =============================================================================

class PersonalizationEngine:
    """
    Service for handling user personalization logic.
    
    Single Responsibility: Only handles personalization
    Open/Closed: Easy to extend with new user types
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
    
    SURPRISE_QUESTIONS: List[str] = [
        "What's Noah's technical background?",
        "Tell me about Noah's MMA fighting experience", 
        "What AI projects has Noah worked on?",
        "How did Noah transition from sales to tech?",
        "What programming languages does Noah know?",
        "What's unique about Noah's career journey?",
        "Can you show me some of Noah's code examples?"
    ]
    
    @classmethod
    def get_welcome_message(cls, user_type: UserType) -> str:
        """Get personalized welcome message for user type."""
        return cls.WELCOME_MESSAGES.get(
            user_type, 
            "Welcome! Ask me anything about Noah."
        )
    
    @classmethod
    def get_random_question(cls) -> str:
        """Get a random surprise question."""
        return random.choice(cls.SURPRISE_QUESTIONS)
    
    @classmethod
    def requires_special_flow(cls, user_type: UserType) -> bool:
        """Check if user type requires special UI flow."""
        return user_type in [UserType.CASUAL_VISITOR, UserType.CRUSH_CONFESSOR]

class SessionManager:
    """
    Centralized session state management with professional patterns.
    
    Benefits:
    - Single source of truth for session state
    - Type-safe operations
    - Easy to test and extend
    """
    
    @staticmethod
    def get_session() -> UserSession:
        """Get or create user session using Singleton pattern."""
        if "user_session" not in st.session_state:
            st.session_state.user_session = UserSession(
                session_id=str(uuid.uuid4())
            )
            logger.info("New user session created")
        return st.session_state.user_session
    
    @staticmethod
    def update_session(session: UserSession) -> None:
        """Update session state with type safety."""
        st.session_state.user_session = session
    
    @staticmethod
    def reset_session() -> None:
        """Reset all session state."""
        session_keys = [key for key in st.session_state.keys() 
                       if key.startswith(('user_', 'show_', 'confession_'))]
        
        for key in session_keys:
            del st.session_state[key]
        
        logger.info("User session reset")

class FileStorageManager:
    """
    Professional file storage service with comprehensive error handling.
    
    Benefits:
    - Consistent error handling across all file operations
    - Directory management and validation
    - Extensible for different storage backends
    - Proper logging for debugging
    """
    
    @staticmethod
    def ensure_directory(path: str) -> bool:
        """Ensure directory exists with proper error handling."""
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Failed to create directory {path}: {e}")
            return False
    
    @staticmethod
    def store_confession(confession: str, anonymous: bool = True, 
                        name: str = "", email: str = "") -> bool:
        """Store user confession with comprehensive error handling."""
        try:
            if not FileStorageManager.ensure_directory("confessions"):
                return False
            
            timestamp = datetime.now().isoformat().replace(':', '-')
            filename = f"confessions/confession_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"=== CONFESSION RECEIVED ===\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write(f"Type: {'Anonymous' if anonymous else 'Open'}\n")
                if not anonymous and name and email:
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
            if not FileStorageManager.ensure_directory("messages"):
                return False
            
            timestamp = datetime.now().isoformat().replace(':', '-')
            filename = f"messages/message_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"=== MESSAGE RECEIVED ===\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write(f"Name: {name}\n")
                f.write(f"Email: {email}\n")
                f.write(f"Subject: {subject}\n")
                f.write(f"\nMessage:\n{message}\n")
            
            logger.info(f"Message stored from: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store message: {e}")
            return False

class ErrorHandler:
    """Centralized error handling with user-friendly messaging."""
    
    @staticmethod
    def handle_qa_error(error: Exception, debug_mode: bool = False) -> None:
        """Handle Q&A processing errors with appropriate user feedback."""
        logger.error(f"Q&A processing failed: {error}")
        st.error("🚨 Sorry, I encountered an error processing your question. Please try again.")
        
        if debug_mode:
            with st.expander("🐛 Debug Information"):
                st.exception(error)
    
    @staticmethod
    def handle_analytics_error(error: Exception) -> None:
        """Handle analytics errors without disrupting user experience."""
        logger.warning(f"Analytics tracking failed: {error}")
        # Silent failure - analytics shouldn't break user experience
    
    @staticmethod
    def handle_storage_error(error: Exception, operation: str) -> None:
        """Handle storage operation errors with user feedback."""
        logger.error(f"Storage operation '{operation}' failed: {error}")
        st.error(f"❌ Failed to {operation}. Please try again.")

# =============================================================================
# UI COMPONENTS - Modular & Reusable
# =============================================================================

class UserSelectionComponent:
    """Professional user selection interface with enhanced UX."""
    
    @staticmethod
    def render() -> Optional[UserType]:
        """
        Render user type selection interface.
        
        Returns:
            Optional[UserType]: Selected user type or None if still selecting
        """
        session = SessionManager.get_session()
        
        # Early return if user already selected
        if session.user_type:
            return session.user_type
        
        # Professional header with clear value proposition
        st.markdown("### 👋 Hello! I'm Noah's AI Assistant")
        st.markdown("*Built with Senior-Level Software Engineering Practices*")
        st.markdown("""
        I'm here to answer questions about Noah's:
        - 🎯 **Career journey** from sales to AI engineering  
        - 💻 **Technical skills** and project experience
        - 🥊 **MMA background** (10 cage fights!)
        - 🚀 **Goals and aspirations** in tech
        - 📈 **Business acumen** and leadership experience
        """)
        
        st.markdown("---")
        st.markdown("**Which best describes you?** *(This helps me personalize responses)*")
        
        # Create elegant button layout with help text
        for user_type in UserType:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if st.button(
                    user_type.value,
                    key=f"select_{user_type.name}",
                    use_container_width=True,
                    help=f"Select this if you are: {user_type.value}"
                ):
                    # Update session with selected type
                    session.user_type = user_type
                    session.app_state = (AppState.SPECIAL_EXPERIENCE 
                                       if PersonalizationEngine.requires_special_flow(user_type)
                                       else AppState.MAIN_CHAT)
                    
                    SessionManager.update_session(session)
                    logger.info(f"User selected: {user_type.value}")
                    st.rerun()
            
            with col2:
                # Add descriptive icons or help text
                help_text = {
                    UserType.HIRING_MANAGER: "Business focus",
                    UserType.TECHNICAL_HIRING_MANAGER: "Technical + Business",
                    UserType.SOFTWARE_DEVELOPER: "Deep technical",
                    UserType.CASUAL_VISITOR: "Fun experience",
                    UserType.CRUSH_CONFESSOR: "Special surprise"
                }
                st.caption(help_text.get(user_type, ""))
        
        return None

class ChatInterface:
    """Professional chat interface with enhanced user experience."""
    
    def __init__(self, config: Config, analytics: ChatbotAnalytics):
        self.config = config
        self.analytics = analytics
        self.app_config = AppConfig()
    
    def render_question_input(self) -> Tuple[Optional[str], bool]:
        """
        Render question input with enhanced UX.
        
        Returns:
            Tuple[Optional[str], bool]: (question, was_surprise_question)
        """
        st.markdown("### 💬 Ask me anything about Noah!")
        
        # Three-column layout for better UX
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            question = st.text_input(
                "Your question:",
                key="user_question",
                placeholder="e.g., What's Noah's technical background?",
                help="Ask about Noah's career, skills, projects, or anything else!"
            )
        
        with col2:
            ask_button = st.button("🚀 Ask", use_container_width=True, type="primary")
        
        with col3:
            surprise_button = st.button("🎲 Surprise Me", use_container_width=True)
        
        # Handle surprise question with immediate feedback
        if surprise_button:
            selected_question = PersonalizationEngine.get_random_question()
            st.session_state.user_question = selected_question
            st.success(f"🎲 Random question: *{selected_question}*")
            return selected_question, True
        
        # Handle normal question
        if ask_button and question and question.strip():
            return question.strip(), False
        
        return None, False
    
    def process_question(self, question: str, qa_chain) -> Optional[Dict[str, Any]]:
        """
        Process question with comprehensive error handling.
        
        Returns:
            Optional[Dict]: Result with response and metadata, or None if error
        """
        try:
            with st.spinner("🤔 Thinking..."):
                start_time = time.time()
                
                # Process with timeout handling
                result = qa_chain.invoke({"query": question})
                response_time = time.time() - start_time
                
                # Validate response
                if not result or "result" not in result:
                    raise ValueError("Invalid response from QA chain")
                
                return {
                    "result": result["result"],
                    "response_time": response_time,
                    "source_documents": result.get("source_documents", [])
                }
                
        except Exception as e:
            ErrorHandler.handle_qa_error(e, self.app_config.debug_mode)
            return None
    
    def display_response(self, question: str, result: Dict[str, Any]) -> None:
        """Display formatted response with professional styling."""
        st.markdown("#### 🤔 Your Question:")
        st.markdown(f"*{question}*")
        
        st.markdown("#### 🤖 Noah's AI Assistant:")
        st.markdown(result["result"])
        
        # Performance metrics for transparency
        col1, col2 = st.columns([2, 1])
        with col2:
            st.metric(
                "Response Time", 
                f"{result['response_time']:.2f}s",
                help="Time taken to generate response"
            )
        
        # Debug information (if enabled)
        if self.app_config.debug_mode and result.get("source_documents"):
            with st.expander("🐛 Debug: Source Documents"):
                for i, doc in enumerate(result["source_documents"], 1):
                    st.markdown(f"**Source {i}:** {doc.page_content[:150]}...")
    
    def track_interaction(self, session: UserSession, question: str, 
                         result: Dict[str, Any]) -> None:
        """Track user interaction with graceful error handling."""
        try:
            if self.app_config.enable_analytics:
                self.analytics.log_question(
                    session_id=session.session_id,
                    user_type=session.user_type.value if session.user_type else "Unknown",
                    question=question,
                    answer=result["result"],
                    response_time=result["response_time"]
                )
                session.questions_asked += 1
                SessionManager.update_session(session)
        except Exception as e:
            ErrorHandler.handle_analytics_error(e)
    
    def render_feedback_section(self, session: UserSession, question: str) -> None:
        """Render feedback section with analytics tracking."""
        st.markdown("---")
        st.markdown("#### 💭 Was this helpful?")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        for i, col in enumerate([col1, col2, col3, col4, col5], 1):
            with col:
                if st.button(
                    "⭐" * i, 
                    help=f"Rate {i}/5 stars", 
                    key=f"rating_{i}_{hash(question)}"  # Unique key per question
                ):
                    try:
                        if self.app_config.enable_analytics:
                            self.analytics.log_feedback(session.session_id, question, i)
                        st.success(f"Thanks! ({i}/5 stars)")
                    except Exception as e:
                        ErrorHandler.handle_analytics_error(e)
    
    def render_popular_questions(self) -> None:
        """Render popular questions section with error handling."""
        try:
            if not self.app_config.enable_analytics:
                return
                
            popular_questions = self.analytics.get_popular_questions(limit=5)
            if not popular_questions:
                return
            
            st.markdown("---")
            st.markdown("### 🔥 Popular Questions")
            st.markdown("*Click on any question to ask it:*")
            
            for i, (question, count) in enumerate(popular_questions, 1):
                if st.button(
                    f"{i}. {question} ({count} times asked)",
                    key=f"popular_{i}",
                    help="Click to ask this question",
                    use_container_width=True
                ):
                    st.session_state.user_question = question
                    st.rerun()
                    
        except Exception as e:
            logger.warning(f"Failed to load popular questions: {e}")

class SpecialExperienceHandler:
    """Handler for special user experiences with modular design."""
    
    @staticmethod
    def render_casual_visitor() -> None:
        """Render complete casual visitor experience."""
        st.markdown("# 🎲 Welcome, Random Visitor! 👋")
        st.markdown("Since you just stumbled upon this, let me give you the fun tour of who Noah is!")
        
        SpecialExperienceHandler._render_career_journey()
        SpecialExperienceHandler._render_mma_highlights()
        SpecialExperienceHandler._render_fun_facts()
        SpecialExperienceHandler._render_contact_section()
        SpecialExperienceHandler._render_easter_egg()
    
    @staticmethod
    def _render_career_journey() -> None:
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
                    st.markdown("🖼️ *[Noah's professional photo]*")
            except:
                st.markdown("🖼️ *[Noah's professional photo]*")
    
    @staticmethod
    def _render_mma_highlights() -> None:
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
    def _render_fun_facts() -> None:
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
    def _render_contact_section() -> None:
        """Render contact section with forms."""
        st.markdown("---")
        st.markdown("## 💬 Want to Connect with Noah?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔗 LinkedIn Profile", use_container_width=True):
                st.markdown("[Connect on LinkedIn](https://www.linkedin.com/in/noah-de-la-calzada-250412358/)")
        
        with col2:
            if st.button("📧 Leave Noah a Message", use_container_width=True):
                st.session_state.show_contact_form = True
        
        if st.session_state.get("show_contact_form", False):
            SpecialExperienceHandler._render_contact_form()
    
    @staticmethod
    def _render_contact_form() -> None:
        """Render contact form with validation."""
        st.markdown("### 📧 Leave Noah a Message")
        
        with st.form("contact_form_casual", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Your Name:", placeholder="John Doe")
            with col2:
                email = st.text_input("Your Email:", placeholder="john@example.com")
            
            subject = st.text_input("Subject:", placeholder="Great AI assistant!")
            message = st.text_area("Your Message:", height=120, 
                                  placeholder="Tell Noah what you think...")
            
            submitted = st.form_submit_button("📤 Send Message", use_container_width=True)
            
            if submitted:
                if all([name.strip(), email.strip(), subject.strip(), message.strip()]):
                    success = FileStorageManager.store_message(
                        name.strip(), email.strip(), subject.strip(), message.strip()
                    )
                    if success:
                        st.success("✅ Message sent to Noah! He'll get back to you soon.")
                        st.session_state.show_contact_form = False
                        st.rerun()
                    else:
                        st.error("❌ Failed to send message. Please try again.")
                else:
                    st.error("📝 Please fill in all fields!")
    
    @staticmethod
    def _render_easter_egg() -> None:
        """Render easter egg message."""
        st.markdown("---")
        st.markdown("*P.S. This AI assistant you're using? Noah built it with senior-level clean architecture principles. Pretty meta, right?* 🤯")
    
    @staticmethod
    def render_crush_confessor() -> None:
        """Render crush confession experience."""
        st.markdown("# 😍 Aww, That's So Sweet! 💕")
        st.markdown("Someone has a crush on Noah! Let me help you with that... 😉")
        
        SpecialExperienceHandler._render_attractive_qualities()
        SpecialExperienceHandler._render_confession_options()
    
    @staticmethod
    def _render_attractive_qualities() -> None:
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
    def _render_confession_options() -> None:
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
        
        confession_type = st.session_state.get("confession_type")
        
        if confession_type == "anonymous":
            SpecialExperienceHandler._render_anonymous_confession()
        elif confession_type == "open":
            SpecialExperienceHandler._render_open_confession()
    
    @staticmethod
    def _render_anonymous_confession() -> None:
        """Render anonymous confession form."""
        st.markdown("---")
        st.markdown("### 🕶️ Anonymous Confession")
        st.markdown("*Your identity will remain completely private!*")
        
        with st.form("anonymous_confession", clear_on_submit=True):
            confession = st.text_area(
                "Share your feelings:",
                placeholder="Tell Noah what you admire about him...",
                height=120
            )
            
            submitted = st.form_submit_button("💌 Send Anonymous Confession", 
                                            use_container_width=True)
            
            if submitted and confession.strip():
                success = FileStorageManager.store_confession(confession.strip(), anonymous=True)
                
                if success:
                    st.success("💕 Your anonymous confession has been sent to Noah!")
                    st.balloons()
                else:
                    st.error("❌ Failed to send confession. Please try again.")
    
    @staticmethod
    def _render_open_confession() -> None:
        """Render open confession form."""
        st.markdown("---")
        st.markdown("### 😊 Open Confession")
        st.markdown("*Let Noah know who you are!*")
        
        with st.form("open_confession", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Your Name:", placeholder="Your name")
            with col2:
                email = st.text_input("Your Email:", placeholder="your@email.com")
            
            confession = st.text_area(
                "Share your feelings:",
                placeholder="Tell Noah what you admire about him and who you are...",
                height=120
            )
            
            consent = st.checkbox("✅ I consent to sharing my contact information with Noah")
            submitted = st.form_submit_button("💌 Send Open Confession", 
                                            use_container_width=True)
            
            if submitted:
                if not all([name.strip(), email.strip(), confession.strip()]):
                    st.error("📝 Please fill in all fields!")
                elif not consent:
                    st.error("⚠️ Please confirm your consent to share contact information.")
                else:
                    success = FileStorageManager.store_confession(
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

class SidebarManager:
    """Professional sidebar management with analytics and information."""
    
    def __init__(self, config: Config, analytics: ChatbotAnalytics):
        self.config = config
        self.analytics = analytics
        self.app_config = AppConfig()
    
    def render(self, session: UserSession) -> None:
        """Render comprehensive sidebar with all information."""
        with st.sidebar:
            self._render_architecture_info()
            self._render_about_section()
            self._render_analytics_section()
            self._render_technical_details()
            self._render_session_controls(session)
    
    def _render_architecture_info(self) -> None:
        """Render architecture improvements section."""
        st.markdown("### 🏗️ Senior-Level Architecture")
        st.markdown("""
        **Professional enhancements:**
        - 🎯 Type-safe enums & dataclasses
        - 🛡️ Comprehensive error handling  
        - 📊 Production-ready logging
        - ⚡ Performance optimizations
        - 🧩 Clean architecture patterns
        - 📝 Junior developer documentation
        """)
    
    def _render_about_section(self) -> None:
        """Render about section."""
        st.markdown("---")
        st.markdown("### 🤖 About This Assistant")
        st.markdown("""
        This AI assistant demonstrates professional software engineering 
        while answering questions about Noah's:
        - 🎯 **Career journey** from sales to AI engineering
        - 💻 **Technical skills** and project experience  
        - 🥊 **MMA background** (10 cage fights!)
        - 🚀 **Goals and aspirations** in tech
        - 📈 **Business acumen** and leadership experience
        """)
    
    def _render_analytics_section(self) -> None:
        """Render analytics section with error handling."""
        if not self.app_config.enable_analytics:
            return
            
        try:
            # Try to get analytics data with fallback methods
            popular_questions = self.analytics.get_popular_questions(limit=3)
            
            st.markdown("---")
            st.markdown("### 📊 Usage Statistics")
            
            # Basic metrics with fallbacks
            col1, col2 = st.columns(2)
            with col1:
                try:
                    # Try to count questions from database
                    with sqlite3.connect(self.analytics.db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT COUNT(*) FROM question_analytics")
                        total_questions = cursor.fetchone()[0]
                        st.metric("Questions", total_questions)
                except:
                    st.metric("Questions", "N/A")
            
            with col2:
                try:
                    # Try to count unique sessions
                    with sqlite3.connect(self.analytics.db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT COUNT(DISTINCT session_id) FROM question_analytics")
                        unique_sessions = cursor.fetchone()[0]
                        st.metric("Users", unique_sessions)
                except:
                    st.metric("Users", "N/A")
            
            try:
                # Try to get average response time
                with sqlite3.connect(self.analytics.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT AVG(response_time_ms) FROM question_analytics WHERE response_time_ms > 0")
                    avg_time = cursor.fetchone()[0]
                    if avg_time:
                        st.metric("Avg Response", f"{avg_time/1000:.1f}s")
            except:
                pass
                
        except Exception as e:
            logger.warning(f"Failed to load analytics: {e}")
    
    def _render_technical_details(self) -> None:
        """Render technical details section."""
        st.markdown("---")
        st.markdown("### 🛠️ Technical Stack")
        try:
            # Get technical details from config with fallbacks
            model_name = getattr(self.config, 'model_name', getattr(self.config, 'OPENAI_MODEL', 'gpt-3.5-turbo'))
            temperature = getattr(self.config, 'temperature', getattr(self.config, 'TEMPERATURE', 0.7))
            max_tokens = getattr(self.config, 'max_tokens', getattr(self.config, 'MAX_TOKENS', 1000))
            
            st.markdown(f"""
            - **AI Model**: {model_name}
            - **Temperature**: {temperature}
            - **Max Tokens**: {max_tokens}
            - **Vector Store**: {getattr(self.config, 'VECTOR_DB_BACKEND', 'FAISS')}
            - **Framework**: Streamlit
            - **Architecture**: Clean & Professional
            """)
        except Exception as e:
            logger.warning(f"Failed to load technical details: {e}")
            st.markdown("""
            - **AI Model**: OpenAI GPT
            - **Vector Store**: FAISS
            - **Framework**: Streamlit
            - **Architecture**: Clean & Professional
            """)
    
    def _render_session_controls(self, session: UserSession) -> None:
        """Render session control buttons."""
        st.markdown("---")
        st.markdown("### ⚙️ Session Controls")
        
        if st.button("🔄 Reset Session", use_container_width=True, 
                    help="Start over with new user type"):
            SessionManager.reset_session()
            st.rerun()
        
        if session.user_type:
            st.markdown(f"**Current User:** {session.user_type.value}")
            st.markdown(f"**Questions Asked:** {session.questions_asked}")
            st.markdown(f"**Session Duration:** {session.session_duration_minutes:.1f} min")

# =============================================================================
# DEPENDENCY INJECTION - Professional Configuration Management
# =============================================================================

class DependencyContainer:
    """
    Dependency injection container for clean architecture.
    
    Benefits:
    - Centralized dependency management
    - Easy testing with mock objects
    - Configuration management
    - Resource caching
    """
    
    @staticmethod
    @st.cache_resource
    def get_config() -> Config:
        """Get cached configuration instance."""
        return Config()
    
    @staticmethod
    @st.cache_resource
    def get_analytics() -> ChatbotAnalytics:
        """Get cached analytics instance."""
        return ChatbotAnalytics()
    
    @staticmethod
    @st.cache_resource(show_spinner=False)
    def get_qa_chain():
        """Get cached QA chain with comprehensive error handling."""
        try:
            from langchain_helper import get_qa_chain
            return get_qa_chain()
        except Exception as e:
            logger.error(f"QA chain initialization failed: {e}")
            return None

# =============================================================================
# MAIN APPLICATION CLASS - Clean Architecture Entry Point
# =============================================================================

class NoahAIAssistantApp:
    """
    Main application class implementing clean architecture principles.
    
    Demonstrates senior-level patterns:
    - Dependency injection
    - Single responsibility
    - Error boundary handling
    - Professional logging
    - State management
    """
    
    def __init__(self):
        """Initialize application with dependency injection."""
        self.config = DependencyContainer.get_config()
        self.analytics = DependencyContainer.get_analytics()
        self.qa_chain = DependencyContainer.get_qa_chain()
        
        # Initialize components with dependencies
        self.chat_interface = ChatInterface(self.config, self.analytics)
        self.sidebar_manager = SidebarManager(self.config, self.analytics)
        
        logger.info("NoahAIAssistantApp initialized successfully")
    
    def configure_page(self) -> None:
        """Configure Streamlit page with professional settings."""
        st.set_page_config(
            page_title="Noah's AI Assistant - Senior Architecture",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render_header(self) -> None:
        """Render professional application header."""
        st.title("Noah's AI Assistant 🤖")
        st.caption("*Demonstrating Senior-Level Generative AI Applications Engineering*")
        
        # Add professional tagline
        with st.expander("🎯 What makes this 'senior-level'?", expanded=False):
            st.markdown("""
            This application demonstrates professional software engineering practices:
            
            - **🏗️ Clean Architecture**: Separation of concerns, service layers, dependency injection
            - **🔒 Type Safety**: Enums, dataclasses, comprehensive type hints
            - **🛡️ Error Handling**: Graceful degradation, user-friendly error messages
            - **📊 Observability**: Professional logging, analytics, performance metrics
            - **🧪 Maintainability**: Modular components, single responsibility, documentation
            - **⚡ Performance**: Smart caching, optimized loading, resource management
            """)
    
    def handle_user_selection(self) -> Optional[UserType]:
        """Handle user type selection phase."""
        return UserSelectionComponent.render()
    
    def handle_special_experience(self, user_type: UserType) -> None:
        """Handle special user experiences."""
        if user_type == UserType.CASUAL_VISITOR:
            SpecialExperienceHandler.render_casual_visitor()
        elif user_type == UserType.CRUSH_CONFESSOR:
            SpecialExperienceHandler.render_crush_confessor()
    
    def handle_main_chat(self, session: UserSession) -> None:
        """Handle main chat interface."""
        if not self.qa_chain:
            st.error("⚠️ Unable to initialize the AI assistant. Please check the configuration.")
            return
        
        # Show personalized welcome message
        welcome_message = PersonalizationEngine.get_welcome_message(session.user_type)
        st.markdown(f"### {welcome_message}")
        
        # Handle question input and processing
        question, was_surprise = self.chat_interface.render_question_input()
        
        if question:
            # Process question
            result = self.chat_interface.process_question(question, self.qa_chain)
            
            if result:
                # Display response
                self.chat_interface.display_response(question, result)
                
                # Track interaction
                self.chat_interface.track_interaction(session, question, result)
                
                # Render feedback and popular questions
                self.chat_interface.render_feedback_section(session, question)
                self.chat_interface.render_popular_questions()
    
    def run(self) -> None:
        """
        Main application entry point with professional error handling.
        
        Implements clean architecture flow:
        1. Configuration and setup
        2. User type selection
        3. Route to appropriate experience
        4. Render sidebar and controls
        """
        try:
            # Configure page
            self.configure_page()
            self.render_header()
            
            # Get user session
            session = SessionManager.get_session()
            
            # Handle user selection phase
            if not session.user_type:
                self.handle_user_selection()
                return
            
            # Route based on user type and app state
            if session.app_state == AppState.SPECIAL_EXPERIENCE:
                self.handle_special_experience(session.user_type)
            else:
                self.handle_main_chat(session)
            
            # Always render sidebar
            self.sidebar_manager.render(session)
            
        except Exception as e:
            # Global error boundary
            logger.critical(f"Critical application error: {e}")
            st.error("🚨 A critical error occurred. Please refresh the page.")
            
            if AppConfig().debug_mode:
                with st.expander("🐛 Debug Information"):
                    st.exception(e)

# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

def main() -> None:
    """
    Professional application entry point.
    
    Demonstrates enterprise-level error handling and application lifecycle management.
    """
    try:
        # Create and run application
        app = NoahAIAssistantApp()
        app.run()
        
    except Exception as e:
        # Ultimate error boundary
        logger.critical(f"Application failed to start: {e}")
        
        st.error("🚨 Critical Error: Application Failed to Start")
        st.markdown("""
        The application encountered a critical error during initialization.
        
        **Possible solutions:**
        - Refresh the page
        - Check your internet connection
        - Verify configuration files exist
        - Contact the developer if the issue persists
        """)
        
        if st.checkbox("Show technical details"):
            st.exception(e)

if __name__ == "__main__":
    main()
