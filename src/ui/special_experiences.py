"""
Special User Experiences
======================

Handles special interactive experiences for casual visitors and crush confessions.
Modular design with clear separation of concerns and reusable components.
"""

import streamlit as st
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
import logging

from ..utils.storage import FileStorageManager

logger = logging.getLogger(__name__)


class ContactFormComponent:
    """Reusable contact form component for message collection."""
    
    @staticmethod
    def render_contact_form(
        context: str = "general",
        default_subject: str = ""
    ) -> Optional[dict]:
        """Render contact form and return submitted data.
        
        Args:
            context: Form context ("general", "confession", etc.)
            default_subject: Default subject line
            
        Returns:
            Optional[dict]: Form data if submitted, None otherwise
        """
        st.markdown("### 📧 Leave Noah a Message")
        
        with st.form(f"contact_form_{context}"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Your Name:")
            with col2:
                email = st.text_input("Your Email:")
            
            subject = st.text_input("Subject:", value=default_subject)
            message = st.text_area(
                "Your Message:",
                height=120,
                placeholder="What would you like to tell Noah?"
            )
            
            submitted = st.form_submit_button("📤 Send Message")
            
            if submitted:
                # Validate form data
                if not all([name.strip(), email.strip(), subject.strip(), message.strip()]):
                    st.error("Please fill in all fields!")
                    return None
                
                return {
                    "name": name.strip(),
                    "email": email.strip(),
                    "subject": subject.strip(),
                    "message": message.strip(),
                    "context": context,
                    "timestamp": datetime.now()
                }
        
        return None


class CasualVisitorExperience:
    """Handles the casual visitor ("Just Randomly Ended Up Here") experience.
    
    Provides an engaging, fun introduction to Noah with career highlights,
    MMA content, and contact options.
    """
    
    @staticmethod
    def render_header() -> None:
        """Render the casual visitor experience header."""
        st.markdown("# 🎲 Welcome, Random Visitor! 👋")
        st.markdown("Since you just stumbled upon this, let me give you the fun tour of who Noah is!")
    
    @staticmethod
    def render_career_overview() -> None:
        """Render Noah's career journey in casual tone."""
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
            CasualVisitorExperience._render_profile_image()
    
    @staticmethod
    def _render_profile_image() -> None:
        """Render profile image if available."""
        try:
            headshot_url = st.secrets.get("HEADSHOT_URL")
            if headshot_url:
                st.image(headshot_url, width=200, caption="The man himself! 😄")
            else:
                st.markdown("🖼️ *[Noah's photo would go here]*")
        except Exception:
            st.markdown("🖼️ *[Noah's photo would go here]*")
    
    @staticmethod
    def render_mma_highlights() -> None:
        """Render MMA highlights section with video."""
        st.markdown("---")
        st.markdown("## 🥊 MMA Highlights - The Good Stuff!")
        st.markdown("**10 cage fights, amateur & professional. Here's the crown jewel:**")
        
        # Title fight details
        st.markdown("### 🏆 Title Fight Victory")
        st.markdown(
            "Noah defeated 5-0 fighter Edgar Sorto to win the "
            "**Fierce Fighting Championship amateur 135-lb title**!"
        )
        
        # Embed YouTube video
        video_url = "https://www.youtube.com/watch?v=MgcAdEoJMzg"
        st.video(video_url)
        
        st.markdown("*Pretty cool for a guy who now codes AI assistants, right?* 😎")
    
    @staticmethod
    def render_fun_facts() -> None:
        """Render fun facts about Noah."""
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
    def render_contact_section() -> None:
        """Render contact section with LinkedIn and message options."""
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
                # Store message form state
                st.session_state.show_contact_form = True
        
        # Render contact form if requested
        if st.session_state.get("show_contact_form", False):
            form_data = ContactFormComponent.render_contact_form(context="casual_visitor")
            
            if form_data:
                storage = FileStorageManager()
                success = storage.store_message(form_data)
                
                if success:
                    st.success("✅ Message sent to Noah! He'll get back to you soon.")
                    st.session_state.show_contact_form = False
                    st.rerun()
                else:
                    st.error("Sorry, there was an issue sending your message. Please try again.")
    
    @staticmethod
    def render_easter_egg() -> None:
        """Render easter egg message."""
        st.markdown("---")
        st.markdown(
            "*P.S. This AI assistant you're using? Noah built it from scratch. Meta, right?* 🤯"
        )
    
    @classmethod
    def render_complete_experience(cls) -> None:
        """Render the complete casual visitor experience."""
        cls.render_header()
        cls.render_career_overview()
        cls.render_mma_highlights()
        cls.render_fun_facts()
        cls.render_contact_section()
        cls.render_easter_egg()


class CrushConfessionExperience:
    """Handles the crush confession experience with anonymous/open options."""
    
    @staticmethod
    def render_header() -> None:
        """Render confession experience header."""
        st.markdown("# 😍 Aww, That's So Sweet! 💕")
        st.markdown("Someone has a crush on Noah! Let me help you with that... 😉")
    
    @staticmethod
    def render_attractive_qualities() -> None:
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
        
        # Show profile image if available
        try:
            headshot_url = st.secrets.get("HEADSHOT_URL")
            if headshot_url:
                st.image(headshot_url, width=250, caption="The object of your affection! 😍")
        except Exception:
            pass
    
    @staticmethod
    def render_confession_options() -> None:
        """Render confession type selection."""
        st.markdown("---")
        st.markdown("## 💌 Ready to Confess?")
        st.markdown("**Would you like to confess anonymously or openly?**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🕶️ Anonymous Confession", use_container_width=True):
                st.session_state.confession_type = "anonymous"
                st.rerun()
                
        with col2:
            if st.button("😊 Open Confession", use_container_width=True):
                st.session_state.confession_type = "open"
                st.rerun()
    
    @staticmethod
    def render_anonymous_confession() -> None:
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
            storage = FileStorageManager()
            success = storage.store_confession({
                "confession": confession.strip(),
                "anonymous": True,
                "timestamp": datetime.now()
            })
            
            if success:
                st.success("💕 Your anonymous confession has been sent to Noah!")
                st.balloons()
                
                # Option for direct message
                if st.button("📝 Leave a Direct Message Too?"):
                    st.session_state.show_confession_contact = True
                    st.rerun()
            else:
                st.error("Sorry, there was an issue sending your confession. Please try again.")
    
    @staticmethod
    def render_open_confession() -> None:
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
                    storage = FileStorageManager()
                    success = storage.store_confession({
                        "confession": confession.strip(),
                        "name": name.strip(),
                        "email": email.strip(),
                        "anonymous": False,
                        "timestamp": datetime.now()
                    })
                    
                    if success:
                        st.success(f"💕 Your confession has been sent to Noah, {name}!")
                        st.balloons()
                    else:
                        st.error("Sorry, there was an issue sending your confession. Please try again.")
    
    @classmethod
    def render_complete_experience(cls) -> None:
        """Render the complete crush confession experience."""
        cls.render_header()
        cls.render_attractive_qualities()
        cls.render_confession_options()
        
        # Handle confession flow based on selection
        confession_type = st.session_state.get("confession_type")
        
        if confession_type == "anonymous":
            cls.render_anonymous_confession()
        elif confession_type == "open":
            cls.render_open_confession()
        
        # Handle follow-up contact form for anonymous confessions
        if st.session_state.get("show_confession_contact", False):
            form_data = ContactFormComponent.render_contact_form(
                context="confession",
                default_subject="Following up on my confession 😊"
            )
            
            if form_data:
                storage = FileStorageManager()
                success = storage.store_message(form_data)
                
                if success:
                    st.success("✅ Message sent to Noah! He'll get back to you soon.")
                    st.session_state.show_confession_contact = False
                    st.rerun()
                else:
                    st.error("Sorry, there was an issue sending your message. Please try again.")