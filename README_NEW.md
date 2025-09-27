# Noah's AI Assistant 🤖

A production-ready RAG (Retrieval-Augmented Generation) powered chatbot built with modern software engineering practices. This AI assistant provides personalized experiences based on user types and showcases clean architecture principles.

## 🏗️ Architecture Overview

This project follows **Clean Architecture** principles with clear separation of concerns:

```
src/
├── core/                    # Business logic & core functionality
│   ├── config.py           # Configuration management with validation
│   ├── rag_engine.py       # RAG implementation with proper abstractions
│   └── analytics_service.py # Analytics and user tracking
├── ui/                     # User interface components
│   ├── user_selection.py   # User type selection logic
│   ├── chat_interface.py   # Main chat interface
│   └── special_experiences.py # Custom user experiences
├── utils/                  # Utility functions
│   └── storage.py          # File-based storage management
└── data/                   # Data persistence layer
```

## 🚀 Features

### Personalized User Experiences
- **🏢 Hiring Manager**: Business-focused content with ROI emphasis
- **💻 Technical Hiring Manager**: Deep technical discussions
- **⚡ Software Developer**: Code examples and implementation details
- **🎲 Casual Visitor**: Fun, engaging experience with MMA highlights
- **😍 Crush Confessor**: Interactive confession system (anonymous/open)

### Enterprise-Grade Features
- **Clean Architecture**: Proper separation of concerns
- **Type Safety**: Comprehensive type hints throughout
- **Error Handling**: Graceful error handling with user-friendly messages
- **Analytics**: User interaction tracking and statistics
- **Caching**: Smart caching for performance optimization
- **Logging**: Comprehensive logging for debugging and monitoring

## 📋 Prerequisites

- **Python 3.8+**
- **OpenAI API Key** (GPT-4 access recommended)
- **Git** for version control

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/noah-ai-assistant.git
cd noah-ai-assistant
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "your-openai-api-key-here"
```

Or set environment variable:
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

### 5. Run the Application
```bash
streamlit run app.py
```

## 📁 Project Structure

### Core Components

#### Configuration Management (`src/core/config.py`)
- **Environment-based configuration** with validation
- **Type-safe configuration classes** using dataclasses
- **Fail-fast validation** with clear error messages
- **Multiple configuration sources** (environment variables, Streamlit secrets)

#### RAG Engine (`src/core/rag_engine.py`)
- **Document processing** with custom CSV loader
- **Vector store management** using FAISS
- **LLM integration** with OpenAI GPT-4
- **Lazy initialization** and caching for performance

#### Analytics Service (`src/core/analytics_service.py`)
- **User interaction tracking** with SQLite backend
- **Analytics statistics** generation
- **Data export capabilities**
- **Privacy-focused design**

### UI Components

#### User Selection (`src/ui/user_selection.py`)
- **Type-safe user type enumeration**
- **Session state management**
- **Personalized welcome messages**
- **User type switching functionality**

#### Chat Interface (`src/ui/chat_interface.py`)
- **Question processing** with proper error handling
- **Response formatting** and display
- **User feedback collection**
- **Popular questions display**

#### Special Experiences (`src/ui/special_experiences.py`)
- **Casual visitor experience** with MMA highlights and YouTube integration
- **Crush confession system** with anonymous/open options
- **Contact form components** with validation

## 🧪 Testing

Run tests (when available):
```bash
python -m pytest tests/
```

## 🐛 Debug Mode

Enable debug mode by setting environment variable:
```bash
export DEBUG=true
```

Debug mode provides:
- Detailed error messages
- Configuration information display
- Source document information
- Enhanced logging

## 📊 Analytics

The application tracks:
- User interactions and response times
- Popular questions and usage patterns
- User type distribution
- Daily usage statistics

View analytics in the admin interface (if implemented) or export data programmatically.

## 🔧 Configuration Options

### OpenAI Settings
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Model to use (default: "gpt-4")
- `OPENAI_TEMPERATURE`: Response creativity (default: 0.1)
- `OPENAI_MAX_TOKENS`: Max response length (default: 1000)

### Application Settings
- `DEBUG`: Enable debug mode (default: false)
- `PAGE_TITLE`: Application title (default: "Noah's AI Assistant")

## 🚀 Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Connect repository in Streamlit Cloud
3. Add secrets in Streamlit Cloud dashboard
4. Deploy

### Local Production
```bash
streamlit run app.py --server.port 8501
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 📈 Performance Optimization

The application includes several performance optimizations:
- **Streamlit caching** for expensive operations
- **Lazy initialization** of components
- **Vector store persistence** to avoid re-indexing
- **Session state management** for user data

## 🧑‍💻 For Developers

### Code Style
- **Type hints** throughout codebase
- **Docstrings** for all public methods
- **Error handling** with specific exception types
- **Logging** for debugging and monitoring

### Adding New User Types
1. Add new enum value to `UserType` in `src/ui/user_selection.py`
2. Add welcome message to `WELCOME_MESSAGES` dict
3. Implement handling logic in appropriate UI component
4. Update documentation

### Adding New Features
1. Follow clean architecture principles
2. Add proper type hints and docstrings
3. Include error handling
4. Add tests for new functionality
5. Update documentation

## 🔒 Security Considerations

- **API keys** stored securely in Streamlit secrets
- **User data** stored locally with privacy in mind
- **Input validation** for all user inputs
- **Error handling** without exposing sensitive information

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

For questions or issues:
1. Check the documentation above
2. Look at existing GitHub issues
3. Create a new issue with detailed description

## 🎯 Future Enhancements

- [ ] Add unit tests with pytest
- [ ] Implement admin dashboard for analytics
- [ ] Add multi-language support
- [ ] Integrate with external APIs
- [ ] Add conversation history
- [ ] Implement user authentication
- [ ] Add CI/CD pipeline

---

Built with ❤️ using clean architecture principles and modern Python practices.