"""
User Selection UI Component
==========================

Handles user type selection and personalization logic.
Clean, reusable component with proper state management.
"""

import streamlit as st
from typing import Dict, Optional
from enum import Enum


class UserType(Enum):
    """User type enumeration for type safety."""
    HIRING_MANAGER = "🏢 Hiring Manager"
    TECHNICAL_HIRING_MANAGER = "💻 Hiring Manager (Technical Background)"
    SOFTWARE_DEVELOPER = "⚡ Software Developer" 
    CASUAL_VISITOR = "🎲 Just Randomly Ended Up Here"
    CRUSH_CONFESSOR = "😍 Looking to Confess You Have a Crush on Noah"


class UserSelectionComponent:
    """Component for handling user type selection and personalization.
    
    Manages user type state, provides personalized welcome messages,
    and handles user type switching functionality.
    """
    
    # Welcome messages for each user type
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
    def initialize_session_state() -> None:
        """Initialize user type in session state if not present."""
        if "user_type" not in st.session_state:
            st.session_state.user_type = None
    
    @staticmethod
    def get_current_user_type() -> Optional[UserType]:
        """Get current user type from session state.
        
        Returns:
            Optional[UserType]: Current user type or None if not selected
        """
        user_type_str = st.session_state.get("user_type")
        if user_type_str:
            # Convert string back to enum
            for user_type in UserType:
                if user_type.value == user_type_str:
                    return user_type
        return None
    
    @staticmethod
    def set_user_type(user_type: UserType) -> None:
        """Set user type in session state.
        
        Args:
            user_type: UserType to set
        """
        st.session_state.user_type = user_type.value
    
    @classmethod
    def render_user_selection(cls) -> bool:
        """Render user type selection interface.
        
        Returns:
            bool: True if user type is selected, False if still selecting
        """
        cls.initialize_session_state()
        
        # Check if user type already selected
        current_user_type = cls.get_current_user_type()
        if current_user_type:
            return True
        
        # Render selection interface
        st.markdown("### 👋 Hello! I'm Noah's AI Assistant")
        st.markdown("In order for me to best assist you, which best describes you?")
        
        # Create buttons for each user type
        for user_type in UserType:
            if st.button(
                user_type.value,
                key=f"user_type_{user_type.name}",
                use_container_width=True
            ):
                cls.set_user_type(user_type)
                st.rerun()
        
        return False  # Still selecting
    
    @classmethod
    def render_welcome_message(cls) -> None:
        """Render personalized welcome message for current user type."""
        current_user_type = cls.get_current_user_type()
        
        if current_user_type and current_user_type in cls.WELCOME_MESSAGES:
            welcome_msg = cls.WELCOME_MESSAGES[current_user_type]
            st.markdown(f"### {welcome_msg}")
    
    @classmethod
    def render_user_type_reset(cls) -> None:
        """Render user type reset button in sidebar."""
        current_user_type = cls.get_current_user_type()
        
        if current_user_type:
            with st.sidebar:
                if st.button("🔄 Change User Type", use_container_width=True):
                    # Clear user type and related session state
                    st.session_state.user_type = None
                    if "user_question" in st.session_state:
                        del st.session_state["user_question"]
                    if "confession_type" in st.session_state:
                        del st.session_state["confession_type"]
                    st.rerun()
    
    @classmethod
    def is_special_user_type(cls) -> bool:
        """Check if current user type requires special handling.
        
        Returns:
            bool: True if special user type (casual visitor or crush confessor)
        """
        current_user_type = cls.get_current_user_type()
        return current_user_type in [UserType.CASUAL_VISITOR, UserType.CRUSH_CONFESSOR]
    
    @classmethod
    def render_user_selection_page(cls) -> Optional[UserType]:
        """Render complete user selection page.
        
        Returns:
            Optional[UserType]: Selected user type or None if still selecting
        """
        # Render user type reset in sidebar
        cls.render_user_type_reset()
        
        # If no user type selected, show selection interface
        if not cls.render_user_selection():
            return None
        
        # Get current user type
        current_user_type = cls.get_current_user_type()
        
        # Render welcome message for non-special user types
        if current_user_type and not cls.is_special_user_type():
            cls.render_welcome_message()
        
        return current_user_type