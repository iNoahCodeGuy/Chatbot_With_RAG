"""
Noah's AI Assistant - Enhanced Architecture Demo
===============================================

This demonstrates clean architecture principles while maintaining compatibility
with the existing codebase. Shows how a senior developer would refactor
for maintainability and clarity.
"""

import streamlit as st
import os
import time
import uuid
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import logging

# Import existing working modules
from config import Config
from analytics import ChatbotAnalytics

# Configure logging for professional monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================================================================
# CLEAN ARCHITECTURE DEMONSTRATION - Type-Safe User Management
# =============================================================================

class UserType(Enum):
    """Type-safe enumeration for user types - prevents string errors."""
    HIRING_MANAGER = "🏢 Hiring Manager"
    TECHNICAL_HIRING_MANAGER = "💻 Hiring Manager (Technical Background)"
    SOFTWARE_DEVELOPER = "⚡ Software Developer"
    CASUAL_VISITOR = "🎲 Just Randomly Ended Up Here"
    CRUSH_CONFESSOR = "😍 Looking to Confess You Have a Crush on Noah"


@dataclass
class UserSession:
    """Data model for user session - demonstrates proper data modeling."""
    session_id: str
    user_type: Optional[UserType] = None
    questions_asked: int = 0
    
    @classmethod
    def get_or_create(cls) -> 'UserSession':
        """Factory method for session management."""
        if "user_session" not in st.session_state:
            st.session_state.user_session = cls(
                session_id=str(uuid.uuid4())
            )
        return st.session_state.user_session


class PersonalizationEngine:
    """Service class for handling user personalization - Single Responsibility Principle."""
    
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
    
    @staticmethod
    def get_welcome_message(user_type: UserType) -> str:
        """Get personalized welcome message for user type."""
        return PersonalizationEngine.WELCOME_MESSAGES.get(
            user_type, "Welcome! Ask me anything about Noah."
        )
    
    @staticmethod
    def is_special_experience(user_type: UserType) -> bool:
        """Check if user type requires special UI flow."""
        return user_type in [UserType.CASUAL_VISITOR, UserType.CRUSH_CONFESSOR]


# =============================================================================
# UI COMPONENTS - Separation of Concerns
# =============================================================================

class UserSelectionComponent:
    """Handles user type selection UI - Component pattern."""
    
    @staticmethod
    def render() -> Optional[UserType]:
        """Render user selection interface and return selected type."""
        session = UserSession.get_or_create()
        
        if session.user_type:
            return session.user_type
        
        st.markdown("### 👋 Hello! I'm Noah's AI Assistant")
        st.markdown("*Built with Clean Architecture & Senior-Level Engineering Practices*")
        st.markdown("In order for me to best assist you, which best describes you?")
        
        # Create buttons for each user type
        for user_type in UserType:
            if st.button(
                user_type.value,
                key=f"select_{user_type.name}",
                use_container_width=True,
                help=PersonalizationEngine.get_welcome_message(user_type)[:100] + "..."
            ):
                session.user_type = user_type
                logger.info(f"User selected type: {user_type.value}")
                st.rerun()
        
        return None
    
    @staticmethod
    def render_reset_button():
        """Render user type reset functionality in sidebar."""
        session = UserSession.get_or_create()
        
        if session.user_type:
            with st.sidebar:
                if st.button("🔄 Change User Type", use_container_width=True):
                    session.user_type = None
                    if "user_question" in st.session_state:
                        del st.session_state["user_question"]
                    logger.info("User reset their type selection")
                    st.rerun()


class ChatInterface:
    """Professional chat interface with proper error handling and analytics."""
    
    def __init__(self, config: Config, analytics: ChatbotAnalytics):
        """Initialize with dependency injection - testable and maintainable."""
        self.config = config
        self.analytics = analytics
    
    def render_question_input(self) -> Optional[str]:
        """Render question input with professional UX."""
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
            ask_clicked = st.button("🚀 Ask", use_container_width=True)
        
        with col3:
            surprise_clicked = st.button("🎲 Surprise Me", use_container_width=True)
        
        if surprise_clicked:
            return self._get_surprise_question()
        
        if ask_clicked and question.strip():
            return question.strip()
        
        return None
    
    def _get_surprise_question(self) -> str:
        """Get a random interesting question - demonstrates private method organization."""
        surprise_questions = [
            "What's Noah's technical background?",
            "Tell me about Noah's MMA fighting experience",
            "What AI projects has Noah worked on?",
            "How did Noah transition from sales to tech?",
            "What programming languages does Noah know?",
            "What's unique about Noah's career journey?",
            "Can you show me some of Noah's code examples?"
        ]
        import random
        return random.choice(surprise_questions)
    
    def process_question(self, question: str, qa_chain) -> Dict[str, Any]:
        """Process question with proper error handling and monitoring."""
        session = UserSession.get_or_create()
        
        try:
            with st.spinner("🤔 Thinking..."):
                start_time = time.time()
                
                result = qa_chain.invoke({"query": question})
                response_time = time.time() - start_time
                
                # Track analytics
                try:
                    self.analytics.log_question(
                        session_id=session.session_id,
                        user_type=session.user_type.value if session.user_type else "Unknown",
                        question=question,
                        answer=result["result"],
                        response_time=response_time
                    )
                    session.questions_asked += 1
                except Exception as e:
                    logger.warning(f"Analytics logging failed: {e}")
                
                return {
                    "answer": result["result"],
                    "sources": result.get("source_documents", []),
                    "response_time": response_time
                }
                
        except Exception as e:
            logger.error(f"Question processing failed: {e}")
            st.error("🚨 Sorry, I encountered an error processing your question. Please try again.")
            return None
    
    def render_response(self, question: str, response_data: Dict[str, Any]):
        """Render response with professional formatting."""
        st.markdown("#### 🤔 Your Question:")
        st.markdown(f"*{question}*")
        
        st.markdown("#### 🤖 Noah's AI Assistant:")
        st.markdown(response_data["answer"])
        
        # Debug mode source display
        if self.config.debug_mode and response_data.get("sources"):
            with st.expander("📚 Sources (Debug Mode)"):
                for i, source in enumerate(response_data["sources"], 1):
                    st.markdown(f"**Source {i}:**")
                    content = source.page_content
                    st.text(content[:200] + "..." if len(content) > 200 else content)


# =============================================================================
# SPECIAL EXPERIENCES - Modular Design
# =============================================================================

class SpecialExperienceHandler:
    """Handles special user experiences - demonstrates strategy pattern."""
    
    @staticmethod
    def render_casual_visitor():
        """Render casual visitor experience."""
        st.markdown("# 🎲 Welcome, Random Visitor! 👋")
        st.markdown("*This demonstrates how clean architecture enables easy feature extension!*")
        st.markdown("Since you just stumbled upon this, let me give you the fun tour of who Noah is!")
        
        # Career overview
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
            st.markdown("🖼️ *[Clean architecture makes adding images easy!]*")
        
        # MMA highlights
        st.markdown("---")
        st.markdown("## 🥊 MMA Highlights - The Good Stuff!")
        st.markdown("**10 cage fights, amateur & professional. Here's the crown jewel:**")
        
        st.markdown("### 🏆 Title Fight Victory")
        st.markdown("Noah defeated 5-0 fighter Edgar Sorto to win the **Fierce Fighting Championship amateur 135-lb title**!")
        
        video_url = "https://www.youtube.com/watch?v=MgcAdEoJMzg"
        st.video(video_url)
        
        st.markdown("*Pretty cool for a guy who now codes with clean architecture principles, right?* 😎")
    
    @staticmethod
    def render_crush_confessor():
        """Render crush confession experience."""
        st.markdown("# 😍 Aww, That's So Sweet! 💕")
        st.markdown("*Even the confession system follows SOLID principles!*")
        st.markdown("Someone has a crush on Noah! Let me help you with that... 😉")
        
        st.markdown("## ✨ What Makes Noah So Crush-Worthy?")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🔥 The Attractive Qualities:**
            - 💪 **MMA Fighter**: 10 cage fights, championship title holder
            - 🧠 **Smart Career Pivot**: Sales → AI Engineering (strategic thinker!)
            - 🚀 **Self-Driven**: Learned coding and clean architecture
            - 💼 **Business Savvy**: Understands both tech and business sides
            - 🎯 **Goal-Oriented**: Clear 3-year vision, works toward it daily
            """)
        
        with col2:
            st.markdown("""
            **😊 The Personality Traits:**
            - 🤝 **Great Communicator**: Bridges technical and non-technical teams
            - 💡 **Problem Solver**: Uses design patterns to solve complex challenges
            - 📈 **Growth Mindset**: Constantly learning (like clean architecture!)
            - 🏆 **Competitive**: But in a healthy, motivating way
            - 🌭 **Fun Side**: Can eat 10 hotdogs in one sitting (impressive!)
            """)
        
        st.markdown("---")
        st.markdown("## 💌 Ready to Confess?")
        st.markdown("*This form could be extended with the strategy pattern for different confession types!*")
        
        confession = st.text_area(
            "Share your feelings:",
            placeholder="Tell Noah what you admire about him (including his clean code!)...",
            height=120
        )
        
        if st.button("💌 Send Confession") and confession.strip():
            st.success("💕 Your confession has been sent! Noah loves clean architecture AND sweet messages!")
            st.balloons()


# =============================================================================
# APPLICATION ORCHESTRATOR - Main App Class
# =============================================================================

class NoahAIAssistantApp:
    """Main application orchestrator - demonstrates clean application structure."""
    
    def __init__(self):
        """Initialize application with proper dependency management."""
        try:
            self.config = self._get_config()
            self.analytics = self._get_analytics()
            self.qa_chain = self._get_qa_chain()
            self.chat_interface = ChatInterface(self.config, self.analytics)
            self.user_selector = UserSelectionComponent()
            logger.info("Application initialized successfully")
        except Exception as e:
            logger.error(f"Application initialization failed: {e}")
            st.error("🚨 Application failed to initialize. Please check your configuration.")
            st.stop()
    
    @staticmethod
    @st.cache_resource
    def _get_config() -> Config:
        """Get cached configuration - demonstrates caching patterns."""
        return Config()
    
    @staticmethod
    @st.cache_resource
    def _get_analytics() -> ChatbotAnalytics:
        """Get cached analytics instance."""
        return ChatbotAnalytics()
    
    @staticmethod
    @st.cache_resource(show_spinner=False)
    def _get_qa_chain():
        """Get cached QA chain with error handling."""
        from langchain_helper import get_qa_chain
        try:
            return get_qa_chain()
        except Exception as e:
            logger.error(f"QA chain initialization failed: {e}")
            return None
    
    def configure_page(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="Noah's AI Assistant - Clean Architecture",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render_header(self):
        """Render professional application header."""
        st.title("Noah's AI Assistant 🤖")
        st.caption("*Demonstrating Clean Architecture & Senior-Level Engineering*")
        
        # Show architecture info
        with st.expander("🏗️ View Clean Architecture Implementation"):
            st.markdown("""
            **This application demonstrates professional software engineering:**
            
            - **🎯 Single Responsibility**: Each class has one clear purpose
            - **🔧 Dependency Injection**: Testable and maintainable code
            - **📝 Type Safety**: Comprehensive type hints throughout
            - **⚡ Performance**: Smart caching and lazy initialization
            - **🛡️ Error Handling**: Graceful error recovery with logging
            - **📊 Analytics**: Professional user interaction tracking
            - **🧩 Modularity**: Easy to extend and modify components
            """)
    
    def run(self):
        """Main application entry point with clean flow control."""
        try:
            self.configure_page()
            self.render_header()
            
            # Handle user selection
            selected_user_type = self.user_selector.render()
            
            if not selected_user_type:
                return  # User still selecting
            
            # Show personalized welcome for regular users
            if not PersonalizationEngine.is_special_experience(selected_user_type):
                welcome_msg = PersonalizationEngine.get_welcome_message(selected_user_type)
                st.markdown(f"### {welcome_msg}")
            
            # Route to appropriate experience
            if selected_user_type == UserType.CASUAL_VISITOR:
                SpecialExperienceHandler.render_casual_visitor()
            elif selected_user_type == UserType.CRUSH_CONFESSOR:
                SpecialExperienceHandler.render_crush_confessor()
            else:
                self._handle_regular_chat()
            
            # Render sidebar components
            self._render_sidebar()
            
            # Render reset button
            self.user_selector.render_reset_button()
            
        except Exception as e:
            logger.error(f"Application runtime error: {e}")
            st.error("🚨 An unexpected error occurred. Please refresh the page.")
            if self.config.debug_mode:
                st.exception(e)
    
    def _handle_regular_chat(self):
        """Handle regular chat flow for professional user types."""
        if not self.qa_chain:
            st.error("⚠️ Unable to initialize the AI assistant. Please check the configuration.")
            return
        
        # Get user question
        question = self.chat_interface.render_question_input()
        
        if question:
            # Process question
            response_data = self.chat_interface.process_question(question, self.qa_chain)
            
            if response_data:
                # Display response
                self.chat_interface.render_response(question, response_data)
                
                # Feedback section
                self._render_feedback_section(question)
    
    def _render_feedback_section(self, question: str):
        """Render user feedback section."""
        st.markdown("---")
        st.markdown("#### 💭 Was this helpful?")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        feedback_given = False
        for i, col in enumerate([col1, col2, col3, col4, col5], 1):
            with col:
                if st.button("⭐" * i, help=f"Rate {i}/5 stars"):
                    try:
                        session = UserSession.get_or_create()
                        self.analytics.log_feedback(session.session_id, question, i)
                        st.success("Thanks for the feedback!")
                        feedback_given = True
                    except Exception as e:
                        logger.warning(f"Feedback logging failed: {e}")
        
        return feedback_given
    
    def _render_sidebar(self):
        """Render informational sidebar with analytics."""
        with st.sidebar:
            st.markdown("### 🏗️ Clean Architecture Demo")
            st.markdown("""
            This application showcases:
            - **Type-safe enums** for user types
            - **Data models** with dataclasses
            - **Service classes** for business logic
            - **Component pattern** for UI elements
            - **Dependency injection** for testability
            - **Proper error handling** throughout
            """)
            
            st.markdown("---")
            st.markdown("### 🤖 About This Assistant")
            st.markdown("""
            Noah's AI assistant with professional features:
            - 🎯 **Career insights** and technical expertise
            - 💻 **Code examples** and architecture discussions
            - 🥊 **MMA background** and personal journey
            - 🚀 **Future goals** in AI and technology
            """)
            
            # Analytics display
            try:
                stats = self.analytics.get_summary_stats()
                st.markdown("---")
                st.markdown("### 📊 Usage Stats")
                st.metric("Total Questions", stats.get("total_questions", 0))
                st.metric("Unique Users", stats.get("unique_sessions", 0))
                if stats.get("avg_response_time"):
                    st.metric("Avg Response", f"{stats['avg_response_time']:.1f}s")
            except Exception:
                pass
            
            # Technical details
            st.markdown("---")
            st.markdown("### 🛠️ Technical Stack")
            st.markdown(f"""
            - **Model**: {self.config.model_name}
            - **Framework**: Streamlit + LangChain
            - **Vector Store**: FAISS
            - **Architecture**: Clean Architecture
            - **Patterns**: Dependency Injection, Strategy
            """)


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

def main():
    """Application entry point with professional error handling."""
    try:
        app = NoahAIAssistantApp()
        app.run()
    except Exception as e:
        logger.critical(f"Critical application error: {e}")
        st.error("🚨 Critical error: Application failed to start.")
        st.exception(e)


if __name__ == "__main__":
    main()