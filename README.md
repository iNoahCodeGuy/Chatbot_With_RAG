# Noah's Portfolio Q&A

An AI-powered Q&A system for Noah's professional portfolio using LangChain, OpenAI, and FAISS with comprehensive analytics tracking.

## ✨ Key Features
- **RAG-powered Q&A** - Retrieval-Augmented Generation over curated knowledge base
- **Smart LinkedIn Integration** - Auto-includes professional profile for career questions  
- **Comprehensive Analytics** - SQLite-based tracking of all interactions and performance metrics
- **Professional UI** - Streamlit interface with sidebar controls and analytics dashboard
- **Zero-config Deployment** - Works out of the box with minimal setup
- **Optimized Performance** - Efficient caching and indexed database queries

## 🚀 Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API key**
   ```bash
   export OPENAI_API_KEY="sk-your-key-here"
   ```
   Or create `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "sk-your-key-here"
   ```

3. **Run the application**
   ```bash
   streamlit run main.py
   ```

4. **Initialize knowledge base** - Click "Create / Refresh Index" in the sidebar, then ask questions!

## ☁️ Deploy on Streamlit Cloud

- **App file**: `main.py`
- **Secrets**: Add `OPENAI_API_KEY` in Streamlit Cloud secrets
- **Optional**: Set `HEADSHOT_URL` and `HEADSHOT_NAME` for profile customization

## ⚙️ Configuration

All settings can be configured via environment variables or Streamlit secrets:

| Setting | Default | Description |
|---------|---------|-------------|
| `OPENAI_MODEL` | `gpt-4` | OpenAI model for responses |
| `OPENAI_TEMPERATURE` | `0.1` | Response creativity (0.0-1.0) |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model |
| `CSV_FILE_PATH` | `noah_portfolio.csv` | Knowledge base file |
| `RETRIEVER_SCORE_THRESHOLD` | `0.7` | Similarity threshold |
| `LINKEDIN_URL` | - | Auto-include for career questions |

## 📁 Project Structure

```
├── main.py                 # Streamlit UI and main application
├── langchain_helper.py     # RAG chain and vector database management
├── analytics.py           # SQLite-based interaction tracking
├── config.py              # Configuration and secrets management
├── noah_portfolio.csv     # Knowledge base (36+ Q&A pairs)
├── requirements.txt       # Python dependencies
├── faiss_index/           # Vector database (auto-generated)
└── archive/               # Legacy Flask files (deprecated)
```

## 📊 Analytics Features

- **Interaction Logging** - All Q&A pairs stored in SQLite
- **Performance Metrics** - Response times and retrieval statistics  
- **Behavioral Analysis** - Career vs general question classification
- **Export Capabilities** - CSV export for external analysis
- **Dashboard View** - Built-in analytics viewer (`analytics_viewer.py`)

## 🛠️ Development

**Run tests**:
```bash
python quick_test.py        # Basic functionality check
python test_system.py       # Comprehensive testing
python final_validation.py  # Full system validation
```

**View analytics**:
```bash
streamlit run analytics_viewer.py
```

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| "OpenAI key present: False" | Set `OPENAI_API_KEY` in secrets or environment |
| Embedding errors | Use default `text-embedding-3-small` model |
| FAISS read error | Click "Create / Refresh Index" to rebuild |
| Import errors | Run `pip install -r requirements.txt` |

## 📖 Documentation

- **[Analytics Guide](ANALYTICS_GUIDE.md)** - Detailed analytics system documentation
- **[Refactoring Summary](REFACTORING_SUMMARY.md)** - Recent improvements and optimizations

## 🔒 Security

- ✅ **No hardcoded secrets** - All API keys via secure configuration
- ✅ **Multi-layer fallback** - Streamlit Secrets → Environment → Local files
- ✅ **Input validation** - Query sanitization and rate limiting
- ✅ **Source attribution** - All responses include traceable references

## 🚀 Performance

- **Cold start**: 2-3 seconds (first query)
- **Warm queries**: <500ms (cached resources)
- **Memory usage**: ~200MB including models
- **Scalability**: Supports 10K+ documents with minimal changes

---

**Built with**: LangChain, OpenAI GPT-4, FAISS, Streamlit, SQLite
