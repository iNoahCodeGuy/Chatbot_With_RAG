"""
Noah's Professional Portfolio Chatbot - Production Flask Application
Advanced logging, analytics, and professional chat interface
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from langchain_helper import get_qa_chain, create_vector_db
from logging_setup import log_chat_event
import os
import time
import uuid
import logging
from datetime import datetime

# Configure application logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enable CORS for cross-origin requests (useful for separate frontend hosting)
CORS(app, origins=["*"])  # Configure origins as needed for production

# Global QA chain for efficient reuse
qa_chain = None

def initialize_qa_chain():
    """Initialize the QA chain with comprehensive error handling"""
    global qa_chain
    try:
        # Check if vector database exists, create if not
        if not os.path.exists('faiss_index'):
            logger.info("🔧 Creating vector database...")
            create_vector_db()
            logger.info("✅ Vector database created successfully!")
        
        qa_chain = get_qa_chain()
        logger.info("✅ QA chain initialized successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error initializing QA chain: {e}")
        return False

def get_client_info(request):
    """Extract client information for logging"""
    return {
        'ip_address': request.headers.get('X-Forwarded-For', request.remote_addr),
        'user_agent': request.headers.get('User-Agent', ''),
        'referrer': request.headers.get('Referer', ''),
        'page': 'chat'  # Can be extended for multiple pages
    }

@app.route('/')
def index():
    """Serve the main portfolio chat interface"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"❌ Error serving index page: {e}")
        return jsonify({'error': 'Failed to load page'}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat API requests with comprehensive logging
    
    Expected JSON payload:
    {
        "message": "User's question",
        "session_id": "unique_session_identifier"
    }
    
    Returns:
    {
        "response": "AI assistant response",
        "session_id": "session_identifier",
        "timestamp": "ISO timestamp"
    }
    """
    start_time = time.time()
    
    try:
        # Validate request data
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get client information for logging
        client_info = get_client_info(request)
        
        # Initialize QA chain if not already done
        global qa_chain
        if qa_chain is None:
            if not initialize_qa_chain():
                logger.error("❌ Failed to initialize QA chain")
                return jsonify({'error': 'Chatbot initialization failed. Please try again later.'}), 500
        
        # Generate AI response
        logger.info(f"💬 Processing question from session {session_id[:8]}...")
        
        try:
            # Use the invoke method instead of deprecated __call__
            response = qa_chain.invoke({'query': user_message})
            ai_response = response.get('result', 'I apologize, but I was unable to generate a response.')
            
        except Exception as e:
            logger.error(f"❌ Error generating AI response: {e}")
            ai_response = "I'm sorry, I encountered an error while processing your question. Please try again."
        
        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)
        
        # Log the interaction
        log_success = log_chat_event(
            session_id=session_id,
            question=user_message,
            answer=ai_response,
            ip_address=client_info['ip_address'],
            user_agent=client_info['user_agent'],
            page=client_info['page'],
            referrer=client_info['referrer'],
            response_time_ms=response_time_ms
        )
        
        if not log_success:
            logger.warning("⚠️ Failed to log chat event, but continuing...")
        
        logger.info(f"✅ Response generated in {response_time_ms}ms for session {session_id[:8]}")
        
        return jsonify({
            'response': ai_response,
            'session_id': session_id,
            'timestamp': datetime.utcnow().isoformat(),
            'response_time_ms': response_time_ms
        })
        
    except Exception as e:
        logger.error(f"❌ Unexpected error in chat endpoint: {e}")
        return jsonify({'error': 'An unexpected error occurred. Please try again.'}), 500

@app.route('/api/initialize', methods=['POST'])
def initialize_knowledge_base():
    """Initialize or recreate the knowledge base"""
    try:
        logger.info("🔧 Initializing knowledge base...")
        create_vector_db()
        
        # Reinitialize QA chain
        global qa_chain
        qa_chain = get_qa_chain()
        
        logger.info("✅ Knowledge base initialized successfully!")
        return jsonify({'message': 'Knowledge base initialized successfully!'})
        
    except Exception as e:
        logger.error(f"❌ Error initializing knowledge base: {e}")
        return jsonify({'error': 'Failed to initialize knowledge base'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check if QA chain is initialized
        chain_status = qa_chain is not None
        
        # Check if vector database exists
        db_exists = os.path.exists('faiss_index')
        
        return jsonify({
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