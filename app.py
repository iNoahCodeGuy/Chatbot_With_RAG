"""""""""

Noah's AI Assistant - Main Application

=====================================Noah's AI Assistant - Main ApplicationNoah's Professional Portfolio Chatbot - Production Flask Application



Production-ready RAG-powered chatbot with clean architecture.=====================================Advanced logging, analytics, and professional chat interface

Entry point for the Streamlit application.

"""

Author: Senior Generative AI Applications Engineer

"""Production-ready RAG-powered chatbot with clean architecture.



import streamlit as stEntry point for the Streamlit application.from flask import Flask, render_template, request, jsonify

import logging

from pathlib import Pathfrom flask_cors import CORS

import sys

Author: Senior Generative AI Applications Engineerfrom langchain_helper import get_qa_chain, create_vector_db

# Add src directory to Python path for imports

src_path = Path(__file__).parent / "src""""from logging_setup import log_chat_event

if str(src_path) not in sys.path:

    sys.path.insert(0, str(src_path))import os



# Import our clean modulesimport streamlit as stimport time

from src.core.config import get_config

from src.core.rag_engine import get_rag_engineimport loggingimport uuid

from src.ui.user_selection import UserSelectionComponent, UserType

from src.ui.chat_interface import ChatInterfaceComponentfrom pathlib import Pathimport logging

from src.ui.special_experiences import CasualVisitorExperience, CrushConfessionExperience

import sysfrom datetime import datetime

# Configure logging

logging.basicConfig(

    level=logging.INFO,

    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'# Add src directory to Python path for imports# Configure application logging

)

logger = logging.getLogger(__name__)src_path = Path(__file__).parent / "src"logging.basicConfig(



if str(src_path) not in sys.path:    level=logging.INFO,

class NoahAIAssistantApp:

    """Main application class orchestrating all components."""    sys.path.insert(0, str(src_path))    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    

    def __init__(self):)

        """Initialize the application with configuration and dependencies."""

        try:# Import our clean moduleslogger = logging.getLogger(__name__)

            self.config = get_config()

            self.rag_engine = get_rag_engine(self.config)from src.core.config import get_config

            self.user_selection = UserSelectionComponent()

            logger.info("Application initialized successfully")from src.core.rag_engine import get_rag_engineapp = Flask(__name__)

        except Exception as e:

            logger.error(f"Application initialization failed: {e}")from src.ui.user_selection import UserSelectionComponent, UserType

            st.error("🚨 Application failed to initialize. Please check your configuration.")

            st.stop()from src.ui.chat_interface import ChatInterfaceComponent# Enable CORS for cross-origin requests (useful for separate frontend hosting)

    

    def configure_page(self) -> None:from src.ui.special_experiences import CasualVisitorExperience, CrushConfessionExperienceCORS(app, origins=["*"])  # Configure origins as needed for production

        """Configure Streamlit page settings."""

        st.set_page_config(from src.utils.logging_config import setup_logging

            page_title=self.config.ui.page_title,

            page_icon=self.config.ui.page_icon,# Global QA chain for efficient reuse

            layout=self.config.ui.layout,

            initial_sidebar_state=self.config.ui.sidebar_state# Configure loggingqa_chain = None

        )

    setup_logging()

    def render_header(self) -> None:

        """Render application header."""logger = logging.getLogger(__name__)def initialize_qa_chain():

        st.title("Noah's AI Assistant 🤖")

        """Initialize the QA chain with comprehensive error handling"""

    def handle_regular_user_experience(self, user_type: UserType) -> None:

        """Handle the regular chat experience for professional user types."""    global qa_chain

        chat_interface = ChatInterfaceComponent(self.config, self.rag_engine)

        chat_interface.render_chat_interface()class NoahAIAssistantApp:    try:

        st.markdown("---")

        chat_interface.render_popular_questions()    """Main application class orchestrating all components.        # Check if vector database exists, create if not

    

    def handle_special_user_experience(self, user_type: UserType) -> None:            if not os.path.exists('faiss_index'):

        """Handle special user experiences."""

        if user_type == UserType.CASUAL_VISITOR:    Follows clean architecture principles with proper separation of concerns.            logger.info("🔧 Creating vector database...")

            CasualVisitorExperience.render_complete_experience()

        elif user_type == UserType.CRUSH_CONFESSOR:    Each component handles its own responsibilities while maintaining            create_vector_db()

            CrushConfessionExperience.render_complete_experience()

        loose coupling through dependency injection.            logger.info("✅ Vector database created successfully!")

    def run(self) -> None:

        """Main application entry point."""    """        

        try:

            self.configure_page()            qa_chain = get_qa_chain()

            self.render_header()

                def __init__(self):        logger.info("✅ QA chain initialized successfully!")

            selected_user_type = self.user_selection.render_user_selection_page()

                    """Initialize the application with configuration and dependencies."""        return True

            if selected_user_type is None:

                return        try:        

            

            if selected_user_type in [UserType.CASUAL_VISITOR, UserType.CRUSH_CONFESSOR]:            self.config = get_config()    except Exception as e:

                self.handle_special_user_experience(selected_user_type)

            else:            self.rag_engine = get_rag_engine(self.config)        logger.error(f"❌ Error initializing QA chain: {e}")

                self.handle_regular_user_experience(selected_user_type)

                            self.user_selection = UserSelectionComponent()        return False

        except Exception as e:

            logger.error(f"Application runtime error: {e}")            logger.info("Application initialized successfully")

            st.error("🚨 An unexpected error occurred. Please refresh the page.")

        except Exception as e:def get_client_info(request):



def main():            logger.error(f"Application initialization failed: {e}")    """Extract client information for logging"""

    """Application entry point."""

    try:            st.error("🚨 Application failed to initialize. Please check your configuration.")    return {

        app = NoahAIAssistantApp()

        app.run()            st.stop()        'ip_address': request.headers.get('X-Forwarded-For', request.remote_addr),

    except Exception as e:

        st.error("🚨 Critical error: Application failed to start.")            'user_agent': request.headers.get('User-Agent', ''),

        st.exception(e)

    def configure_page(self) -> None:        'referrer': request.headers.get('Referer', ''),



if __name__ == "__main__":        """Configure Streamlit page settings."""        'page': 'chat'  # Can be extended for multiple pages

    main()
        st.set_page_config(    }

            page_title=self.config.ui.page_title,

            page_icon=self.config.ui.page_icon,@app.route('/')

            layout=self.config.ui.layout,def index():

            initial_sidebar_state=self.config.ui.sidebar_state    """Serve the main portfolio chat interface"""

        )    try:

            return render_template('index.html')

    def render_header(self) -> None:    except Exception as e:

        """Render application header."""        logger.error(f"❌ Error serving index page: {e}")

        st.title("Noah's AI Assistant 🤖")        return jsonify({'error': 'Failed to load page'}), 500

        

        # Add debug info if in debug mode@app.route('/api/chat', methods=['POST'])

        if self.config.debug_mode:def chat():

            st.caption("🐛 Debug mode enabled")    """

        Handle chat API requests with comprehensive logging

    def handle_regular_user_experience(self, user_type: UserType) -> None:    

        """Handle the regular chat experience for professional user types.    Expected JSON payload:

            {

        Args:        "message": "User's question",

            user_type: The current user type        "session_id": "unique_session_identifier"

        """    }

        # Create and render chat interface    

        chat_interface = ChatInterfaceComponent(self.config, self.rag_engine)    Returns:

            {

        # Render main chat interface        "response": "AI assistant response",

        chat_interface.render_chat_interface()        "session_id": "session_identifier",

                "timestamp": "ISO timestamp"

        # Add some spacing    }

        st.markdown("---")    """

            start_time = time.time()

        # Render popular questions (helps users discover content)    

        chat_interface.render_popular_questions()    try:

            # Validate request data

    def handle_special_user_experience(self, user_type: UserType) -> None:        if not request.is_json:

        """Handle special user experiences.            return jsonify({'error': 'Request must be JSON'}), 400

                

        Args:        data = request.get_json()

            user_type: The special user type requiring custom experience        user_message = data.get('message', '').strip()

        """        session_id = data.get('session_id', str(uuid.uuid4()))

        if user_type == UserType.CASUAL_VISITOR:        

            CasualVisitorExperience.render_complete_experience()        if not user_message:

        elif user_type == UserType.CRUSH_CONFESSOR:            return jsonify({'error': 'Message cannot be empty'}), 400

            CrushConfessionExperience.render_complete_experience()        

        else:        # Get client information for logging

            # Fallback - should not happen        client_info = get_client_info(request)

            logger.warning(f"Unknown special user type: {user_type}")        

            st.error("Unknown user type. Please refresh and try again.")        # Initialize QA chain if not already done

            global qa_chain

    def render_sidebar_info(self) -> None:        if qa_chain is None:

        """Render informational sidebar."""            if not initialize_qa_chain():

        with st.sidebar:                logger.error("❌ Failed to initialize QA chain")

            st.markdown("### 🤖 About This Assistant")                return jsonify({'error': 'Chatbot initialization failed. Please try again later.'}), 500

            st.markdown("""        

            This AI assistant knows all about Noah's:        # Generate AI response

            - 🎯 **Career journey** from sales to AI engineering        logger.info(f"💬 Processing question from session {session_id[:8]}...")

            - 💻 **Technical skills** and project experience          

            - 🥊 **MMA background** (10 cage fights!)        try:

            - 🚀 **Goals and aspirations** in tech            # Use the invoke method instead of deprecated __call__

            - 📈 **Business acumen** and leadership experience            response = qa_chain.invoke({'query': user_message})

            """)            ai_response = response.get('result', 'I apologize, but I was unable to generate a response.')

                        

            st.markdown("---")        except Exception as e:

            st.markdown("### 🛠️ Built With")            logger.error(f"❌ Error generating AI response: {e}")

            st.markdown("""            ai_response = "I'm sorry, I encountered an error while processing your question. Please try again."

            - **LangChain** for RAG orchestration        

            - **OpenAI GPT-4** for responses        # Calculate response time

            - **FAISS** for vector search        response_time_ms = int((time.time() - start_time) * 1000)

            - **Streamlit** for the interface        

            - **Clean Architecture** principles        # Log the interaction

            """)        log_success = log_chat_event(

                        session_id=session_id,

            if self.config.debug_mode:            question=user_message,

                st.markdown("---")            answer=ai_response,

                st.markdown("### 🐛 Debug Info")            ip_address=client_info['ip_address'],

                st.json({            user_agent=client_info['user_agent'],

                    "Model": self.config.openai.model,            page=client_info['page'],

                    "Temperature": self.config.openai.temperature,            referrer=client_info['referrer'],

                    "Max Tokens": self.config.openai.max_tokens            response_time_ms=response_time_ms

                })        )

            

    def run(self) -> None:        if not log_success:

        """Main application entry point."""            logger.warning("⚠️ Failed to log chat event, but continuing...")

        try:        

            # Configure page        logger.info(f"✅ Response generated in {response_time_ms}ms for session {session_id[:8]}")

            self.configure_page()        

                    return jsonify({

            # Render header            'response': ai_response,

            self.render_header()            'session_id': session_id,

                        'timestamp': datetime.utcnow().isoformat(),

            # Handle user type selection and routing            'response_time_ms': response_time_ms

            selected_user_type = self.user_selection.render_user_selection_page()        })

                    

            if selected_user_type is None:    except Exception as e:

                # User is still selecting their type        logger.error(f"❌ Unexpected error in chat endpoint: {e}")

                return        return jsonify({'error': 'An unexpected error occurred. Please try again.'}), 500

            

            # Route to appropriate experience based on user type@app.route('/api/initialize', methods=['POST'])

            if selected_user_type in [UserType.CASUAL_VISITOR, UserType.CRUSH_CONFESSOR]:def initialize_knowledge_base():

                self.handle_special_user_experience(selected_user_type)    """Initialize or recreate the knowledge base"""

            else:    try:

                self.handle_regular_user_experience(selected_user_type)        logger.info("🔧 Initializing knowledge base...")

                    create_vector_db()

            # Render sidebar info        

            self.render_sidebar_info()        # Reinitialize QA chain

                    global qa_chain

        except Exception as e:        qa_chain = get_qa_chain()

            logger.error(f"Application runtime error: {e}")        

            st.error("🚨 An unexpected error occurred. Please refresh the page.")        logger.info("✅ Knowledge base initialized successfully!")

                    return jsonify({'message': 'Knowledge base initialized successfully!'})

            if self.config.debug_mode:        

                st.exception(e)    except Exception as e:

        logger.error(f"❌ Error initializing knowledge base: {e}")

        return jsonify({'error': 'Failed to initialize knowledge base'}), 500

def main():

    """Application entry point."""@app.route('/api/health')

    try:def health_check():

        app = NoahAIAssistantApp()    """Health check endpoint for monitoring"""

        app.run()    try:

    except Exception as e:        # Check if QA chain is initialized

        st.error("🚨 Critical error: Application failed to start.")        chain_status = qa_chain is not None

        st.exception(e)        

        # Check if vector database exists

        db_exists = os.path.exists('faiss_index')

if __name__ == "__main__":        

    main()        return jsonify({
            'status': 'healthy' if chain_status and db_exists else 'degraded',
            'qa_chain_initialized': chain_status,
            'vector_db_exists': db_exists,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get basic chat statistics (for admin/monitoring)"""
    try:
        from logging_setup import chat_logger
        
        # Get today's stats
        daily_stats = chat_logger.get_daily_stats()
        
        return jsonify({
            'daily_stats': daily_stats,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Error getting stats: {e}")
        return jsonify({'error': 'Failed to retrieve statistics'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"❌ Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting Noah's Portfolio Chatbot...")
    
    # Initialize QA chain on startup (optional - will initialize on first request if needed)
    initialize_qa_chain()
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )