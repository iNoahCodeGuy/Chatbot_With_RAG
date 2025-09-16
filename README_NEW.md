# Portfolio Q&A System

An intelligent question-answering system that allows hiring managers to ask questions about Noah's professional background using OpenAI's GPT-4 and vector search technology.

## Features

- 🤖 **AI-Powered Q&A**: Uses GPT-4 for intelligent responses
- 🔍 **Semantic Search**: Vector-based search using OpenAI embeddings
- 📊 **Professional Data**: Loads from CSV containing professional experience
- 🔧 **Configurable**: Environment-based configuration management
- 📱 **Multiple Interfaces**: Jupyter notebook, Python scripts, and web interface

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. **Clone/Download** this repository

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env file and add your OpenAI API key
   ```

3. **Run setup script**:
   ```bash
   python setup.py
   ```

### Manual Installation

If you prefer manual setup:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`

3. **Initialize vector database**:
   ```python
   from langchain_helper import create_vector_db
   create_vector_db()
   ```

## Usage

### Jupyter Notebook
Open `openai_codebasics_q_and_a.ipynb` and run the cells to see examples.

### Python Script
```python
from langchain_helper import get_qa_chain

# Initialize the Q&A system
chain = get_qa_chain()

# Ask questions about Noah's background
result = chain("What is Noah's professional background?")
print(result['result'])
```

### Web Interface (if Streamlit is installed)
```bash
streamlit run main.py
```

## Configuration

The system uses environment variables for configuration:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | *required* | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4` | OpenAI model to use |
| `OPENAI_TEMPERATURE` | `0.1` | Response creativity (0-1) |
| `CSV_FILE_PATH` | `noah_portfolio.csv` | Path to portfolio data |
| `RETRIEVER_SCORE_THRESHOLD` | `0.7` | Search similarity threshold |

## Data Format

Update `noah_portfolio.csv` with your professional information:

```csv
question,answer
"What is your background?","I have 5+ years in software development..."
"What are your skills?","Python, JavaScript, AI/ML, cloud platforms..."
```

## Project Structure

```
📁 3_project_codebasics_q_and_a/
├── 📄 .env                           # Environment variables (not in git)
├── 📄 .env.example                   # Environment template
├── 📄 .gitignore                     # Git ignore rules
├── 📄 config.py                      # Configuration management
├── 📄 langchain_helper.py            # Core Q&A functionality
├── 📄 noah_portfolio.csv             # Professional data
├── 📄 requirements.txt               # Python dependencies
├── 📄 setup.py                       # Setup script
├── 📄 openai_codebasics_q_and_a.ipynb # Jupyter notebook
├── 📁 faiss_index/                  # Vector database (auto-created)
└── 📄 README.md                      # This file
```

## Best Practices

- ✅ API keys stored in environment variables
- ✅ Configuration centralized in `config.py`
- ✅ Modern package versions
- ✅ Proper gitignore for security
- ✅ Documentation and examples
- ✅ Error handling and validation

## Troubleshooting

### Common Issues

**Import Errors**: Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

**API Key Issues**: Verify your `.env` file has a valid OpenAI API key

**Vector Database Issues**: Delete `faiss_index/` folder and run setup again

## Contributing

1. Update your professional data in `noah_portfolio.csv`
2. Modify prompts in `langchain_helper.py` if needed
3. Test changes with the Jupyter notebook
4. Update configuration in `config.py` as needed

## License

This project is for personal portfolio use.