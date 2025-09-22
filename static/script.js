// Noah's Portfolio Chatbot JavaScript

class PortfolioChatbot {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.questionInput = document.getElementById('questionInput');
        this.sendButton = document.getElementById('sendButton');
        this.initializeBtn = document.getElementById('initializeBtn');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Send button click
        this.sendButton.addEventListener('click', () => this.sendQuestion());
        
        // Enter key press
        this.questionInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendQuestion();
            }
        });
        
        // Initialize button click
        this.initializeBtn.addEventListener('click', () => this.initializeKnowledgeBase());
        
        // Auto-focus on input
        this.questionInput.focus();
    }

    async sendQuestion() {
        const question = this.questionInput.value.trim();
        
        if (!question) {
            this.showError('Please enter a question.');
            return;
        }

        // Disable input while processing
        this.setInputState(false);
        this.showLoading(true);

        // Add user message to chat
        this.addMessage(question, 'user');
        this.questionInput.value = '';

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question })
            });

            const data = await response.json();

            if (response.ok) {
                this.addMessage(data.answer, 'bot');
            } else {
                this.addMessage(`Error: ${data.error || 'Failed to get response'}`, 'bot', true);
            }
        } catch (error) {
            console.error('Error:', error);
            this.addMessage('Sorry, there was an error connecting to the server. Please try again.', 'bot', true);
        } finally {
            this.setInputState(true);
            this.showLoading(false);
        }
    }

    async initializeKnowledgeBase() {
        this.initializeBtn.disabled = true;
        this.initializeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Initializing...';

        try {
            const response = await fetch('/initialize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (response.ok) {
                this.showSuccess('Knowledge base initialized successfully!');
                this.addMessage('Great! The knowledge base has been updated. You can now ask questions about Noah\'s professional background.', 'bot');
            } else {
                this.showError(data.error || 'Failed to initialize knowledge base');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError('Failed to initialize knowledge base. Please try again.');
        } finally {
            this.initializeBtn.disabled = false;
            this.initializeBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Initialize Knowledge Base';
        }
    }

    addMessage(content, sender, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message${isError ? ' error-message' : ''}`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // Format the content with basic markdown-like formatting
        const formattedContent = this.formatMessage(content);
        contentDiv.innerHTML = `<p>${formattedContent}</p>`;
        
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    formatMessage(content) {
        // Basic formatting for better readability
        return content
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>');
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    setInputState(enabled) {
        this.questionInput.disabled = !enabled;
        this.sendButton.disabled = !enabled;
        
        if (enabled) {
            this.questionInput.focus();
        }
    }

    showLoading(show) {
        this.loadingOverlay.style.display = show ? 'flex' : 'none';
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas ${type === 'error' ? 'fa-exclamation-circle' : 'fa-check-circle'}"></i>
                <span>${message}</span>
            </div>
        `;

        // Add to DOM
        document.body.appendChild(notification);

        // Show animation
        setTimeout(() => notification.classList.add('show'), 100);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 5000);
    }
}

// Global functions for HTML onclick handlers
function askQuestion(question) {
    const chatbot = window.portfolioChatbot;
    if (chatbot) {
        chatbot.questionInput.value = question;
        chatbot.sendQuestion();
    }
}

function sendQuestion() {
    const chatbot = window.portfolioChatbot;
    if (chatbot) {
        chatbot.sendQuestion();
    }
}

function initializeKnowledgeBase() {
    const chatbot = window.portfolioChatbot;
    if (chatbot) {
        chatbot.initializeKnowledgeBase();
    }
}

// Initialize the chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.portfolioChatbot = new PortfolioChatbot();
    
    // Handle headshot placeholder
    const headshot = document.getElementById('headshot');
    if (headshot) {
        headshot.onerror = function() {
            // If headshot image fails to load, show a professional placeholder
            this.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDEyMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxMjAiIGhlaWdodD0iMTIwIiByeD0iNjAiIGZpbGw9IiM2NjdlZWEiLz4KPHN2ZyB4PSIzMCIgeT0iMzAiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJ3aGl0ZSI+CjxwYXRoIGQ9Ik0xMiAyQzEzLjEgMiAxNCAxNC45IDE0IDEyQzE0IDEzLjEgMTMuMSAxNCAxMiAxNEM5LjkgMTQgOSAxMy4xIDkgMTJDOSAxMC45IDkuOSAxMCAxMCAxMEMxMC4xIDEwIDExIDEwLjkgMTIgMloiLz4KPHN0eWxlPgogIC5zdDAge2ZpbGw6I0ZGRkZGRjt9Cjwvc3R5bGU+CjwvZz4KPC9zdmc+';
            this.style.backgroundColor = '#667eea';
            this.style.display = 'flex';
            this.style.alignItems = 'center';
            this.style.justifyContent = 'center';
            this.style.fontSize = '3rem';
            this.style.color = 'white';
            this.innerHTML = 'N';
        };
    }
});

// Add notification styles dynamically
const notificationStyles = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        z-index: 1001;
        max-width: 400px;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
    }
    
    .notification.show {
        opacity: 1;
        transform: translateX(0);
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem 1.25rem;
    }
    
    .notification-error {
        border-left: 4px solid #ef4444;
        color: #dc2626;
    }
    
    .notification-success {
        border-left: 4px solid #10b981;
        color: #059669;
    }
    
    .notification-info {
        border-left: 4px solid #3b82f6;
        color: #2563eb;
    }
`;

// Add styles to document head
const styleElement = document.createElement('style');
styleElement.textContent = notificationStyles;
document.head.appendChild(styleElement);