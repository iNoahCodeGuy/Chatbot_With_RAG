"""
Chat Interface Component
=======================

Main chat interface for handling user questions and displaying responses.
Clean, professional interface with proper state management and error handling.
"""

import streamlit as st
import time
from typing import Optional, Dict, Any
import logging

from ..core.rag_engine import RAGEngine
from ..core.config import AppConfig
from ..core.analytics_service import get_analytics_service

logger = logging.getLogger(__name__)


class ChatInterfaceComponent:
    """Main chat interface component for user interaction.
    
    Handles question input, response generation, display formatting,
    and analytics tracking with proper error handling.
    """
    
    def __init__(self, config: AppConfig, rag_engine: RAGEngine):
        """Initialize chat interface.
        
        Args:
            config: Application configuration
            rag_engine: RAG engine instance
        """
        self.config = config
        self.rag_engine = rag_engine
        self.analytics = get_analytics_service()
    
    def _get_session_id(self) -> str:
        """Get or create session ID for analytics tracking.
        
        Returns:
            str: Session ID
        """
        if "session_id" not in st.session_state:
            import uuid
            st.session_state.session_id = str(uuid.uuid4())
        return st.session_state.session_id
    
    def _get_user_type_for_analytics(self) -> str:
        """Get user type string for analytics.
        
        Returns:
            str: User type for analytics
        """
        return st.session_state.get("user_type", "Unknown")
    
    def render_question_input(self) -> Optional[str]:
        """Render question input interface.
        
        Returns:
            Optional[str]: User's question if submitted, None otherwise
        """
        st.markdown("### 💬 Ask me anything about Noah!")
        
        # Text input for question
        question = st.text_input(
            "Your question:",
            key="user_question",
            placeholder="e.g., What's Noah's technical background?",
            help="Ask about Noah's career, skills, projects, or anything else!"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("🚀 Ask", use_container_width=True):
                if question.strip():
                    return question.strip()
                else:
                    st.warning("Please enter a question!")
        
        with col2:
            if st.button("🎲 Surprise Me", use_container_width=True):
                # Return a random interesting question
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
        
        return None
    
    def render_response(self, question: str, response_data: Dict[str, Any]) -> None:
        """Render question response with proper formatting.
        
        Args:
            question: User's question
            response_data: Response data from RAG engine
        """
        # Display question
        st.markdown("#### 🤔 Your Question:")
        st.markdown(f"*{question}*")
        
        # Display answer
        st.markdown("#### 🤖 Noah's AI Assistant:")
        
        # Format and display the answer
        answer = response_data.get("answer", "I'm sorry, I couldn't generate a response.")
        st.markdown(answer)
        
        # Optional: Display sources (for debugging or transparency)
        if self.config.debug_mode and "sources" in response_data:
            with st.expander("📚 Sources (Debug Mode)"):
                sources = response_data["sources"]
                if sources:
                    for i, source in enumerate(sources, 1):
                        st.markdown(f"**Source {i}:**")
                        st.text(source.page_content[:200] + "..." if len(source.page_content) > 200 else source.page_content)
                else:
                    st.markdown("No sources available.")
    
    def render_feedback_section(self, question: str) -> Optional[int]:
        """Render feedback collection section.
        
        Args:
            question: The question that was asked
            
        Returns:
            Optional[int]: User rating if provided
        """
        st.markdown("---")
        st.markdown("#### 💭 Was this helpful?")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        rating = None
        
        with col1:
            if st.button("⭐", help="Poor"):
                rating = 1
        with col2:
            if st.button("⭐⭐", help="Fair"):
                rating = 2
        with col3:
            if st.button("⭐⭐⭐", help="Good"):
                rating = 3
        with col4:
            if st.button("⭐⭐⭐⭐", help="Very Good"):
                rating = 4
        with col5:
            if st.button("⭐⭐⭐⭐⭐", help="Excellent"):
                rating = 5
        
        if rating:
            st.success(f"Thanks for the feedback! ({rating}/5 stars)")
        
        return rating
    
    def process_question(self, question: str) -> Optional[Dict[str, Any]]:
        """Process user question and return response data.
        
        Args:
            question: User's question
            
        Returns:
            Optional[Dict[str, Any]]: Response data or None if error
        """
        try:
            # Show processing spinner
            with st.spinner("🤔 Thinking..."):
                start_time = time.time()
                
                # Get response from RAG engine
                response_data = self.rag_engine.query(question)
                
                response_time = time.time() - start_time
                response_data["response_time"] = response_time
                
                return response_data
                
        except Exception as e:
            logger.error(f"Error processing question: {e}")
            st.error(
                "🚨 Oops! Something went wrong while processing your question. "
                "Please try again or rephrase your question."
            )
            return None
    
    def track_interaction(
        self, 
        question: str, 
        answer: str, 
        response_time: float, 
        rating: Optional[int] = None
    ) -> None:
        """Track user interaction for analytics.
        
        Args:
            question: User's question
            answer: AI's response
            response_time: Time taken to generate response
            rating: Optional user rating
        """
        try:
            self.analytics.track_question(
                session_id=self._get_session_id(),
                user_type=self._get_user_type_for_analytics(),
                question=question,
                answer=answer,
                response_time=response_time,
                user_rating=rating
            )
        except Exception as e:
            logger.warning(f"Failed to track interaction: {e}")
            # Don't fail the user experience for analytics issues
    
    def render_chat_interface(self) -> None:
        """Render the complete chat interface."""
        # Get user question
        question = self.render_question_input()
        
        if question:
            # Process the question
            response_data = self.process_question(question)
            
            if response_data:
                # Display response
                self.render_response(question, response_data)
                
                # Get user feedback
                rating = self.render_feedback_section(question)
                
                # Track interaction
                self.track_interaction(
                    question=question,
                    answer=response_data.get("answer", ""),
                    response_time=response_data.get("response_time", 0.0),
                    rating=rating
                )
                
                # Clear the question input for next question
                if rating:  # Only clear after rating is given
                    st.session_state.user_question = ""
                    st.rerun()
    
    def render_popular_questions(self) -> None:
        """Render popular questions section."""
        try:
            stats = self.analytics.get_stats(days=30)
            popular_questions = stats.popular_questions[:5]  # Top 5
            
            if popular_questions:
                st.markdown("### 🔥 Popular Questions")
                st.markdown("*Click on any question to ask it:*")
                
                for i, q_data in enumerate(popular_questions, 1):
                    question = q_data["question"]
                    count = q_data["count"]
                    
                    if st.button(
                        f"{i}. {question} ({count} times asked)",
                        key=f"popular_q_{i}",
                        help="Click to ask this question"
                    ):
                        # Set the question and process it
                        st.session_state.user_question = question
                        st.rerun()
                        
        except Exception as e:
            logger.warning(f"Failed to load popular questions: {e}")
            # Don't show the section if there's an error