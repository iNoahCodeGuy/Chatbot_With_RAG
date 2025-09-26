"""
LangChain Helper Utilities
==========================

Production-ready utilities for RAG (Retrieval-Augmented Generation) pipeline
with lazy initialization, comprehensive error handling, and enterprise patterns.

Key Features:
- Lazy resource initialization to prevent startup failures
- Multi-backend vector database support (FAISS + Chroma fallback)
- Professional prompt engineering with LinkedIn integration
- Comprehensive configuration validation
- Thread-safe singleton patterns

Author: Senior Generative AI Applications Engineer
"""

import os
from typing import Optional
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from config import config

# Optional Chroma fallback support
try:
    from langchain_community.vectorstores import Chroma
    HAS_CHROMA = True
except ImportError:
    HAS_CHROMA = False

# Global singletons for thread safety and performance
_llm_instance: Optional[ChatOpenAI] = None
_embeddings_instance: Optional[OpenAIEmbeddings] = None


def _ensure_config_valid() -> None:
    """Validate configuration with clear error messages."""
    try:
        config.validate()
    except Exception as e:
        raise RuntimeError(f"Configuration validation failed: {e}")


def _get_llm() -> ChatOpenAI:
    """Get or create ChatOpenAI instance with lazy initialization."""
    global _llm_instance
    if _llm_instance is None:
        _ensure_config_valid()
        _llm_instance = ChatOpenAI(
            model=config.OPENAI_MODEL,
            temperature=config.OPENAI_TEMPERATURE,
            api_key=config.OPENAI_API_KEY,
        )
    return _llm_instance


def _get_embeddings() -> OpenAIEmbeddings:
    """Get or create OpenAI embeddings instance with lazy initialization."""
    global _embeddings_instance
    if _embeddings_instance is None:
        _ensure_config_valid()
        try:
            _embeddings_instance = OpenAIEmbeddings(
                model=config.OPENAI_EMBEDDING_MODEL,
                api_key=config.OPENAI_API_KEY,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize OpenAI embeddings: {e}")
    return _embeddings_instance


def vector_db_exists() -> bool:
    """Check if the FAISS vector database exists on disk."""
    vectordb_path = config.VECTOR_DB_PATH
    faiss_index = os.path.join(vectordb_path, "index.faiss")
    faiss_pkl = os.path.join(vectordb_path, "index.pkl")
    return os.path.exists(faiss_index) and os.path.exists(faiss_pkl)


def _load_portfolio_documents():
    """Load and return documents from the portfolio CSV file."""
    if not os.path.exists(config.CSV_FILE_PATH):
        raise FileNotFoundError(f"Portfolio CSV not found: {config.CSV_FILE_PATH}")
    
    loader = CSVLoader(
        file_path=config.CSV_FILE_PATH,
        source_column=config.SOURCE_COLUMN,
    )
    documents = loader.load()
    
    if not documents:
        raise ValueError("No documents loaded from CSV file")
    
    return documents


def _create_faiss_index(documents):
    """Create and persist FAISS vector index."""
    vectordb = FAISS.from_documents(
        documents=documents,
        embedding=_get_embeddings(),
    )
    
    # Ensure directory exists
    os.makedirs(config.VECTOR_DB_PATH, exist_ok=True)
    vectordb.save_local(config.VECTOR_DB_PATH)
    
    return vectordb


def _create_chroma_index(documents):
    """Create and persist Chroma vector index as fallback."""
    if not HAS_CHROMA:
        raise RuntimeError(
            "Chroma not available. Install with: pip install chromadb"
        )
    
    os.makedirs(config.CHROMA_DB_PATH, exist_ok=True)
    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=_get_embeddings(),
        persist_directory=config.CHROMA_DB_PATH,
    )
    vectordb.persist()
    return vectordb


def create_vector_db() -> None:
    """
    Build and persist vector database from portfolio CSV.
    
    Supports FAISS (primary) with Chroma fallback for maximum compatibility.
    Automatically creates necessary directories and handles errors gracefully.
    """
    _ensure_config_valid()
    documents = _load_portfolio_documents()
    
    backend = getattr(config, "VECTOR_DB_BACKEND", "faiss").lower()
    
    if backend == "faiss":
        try:
            _create_faiss_index(documents)
            return
        except Exception as faiss_error:
            if HAS_CHROMA:
                print(f"FAISS failed ({faiss_error}), falling back to Chroma...")
                _create_chroma_index(documents)
                return
            raise RuntimeError(f"FAISS failed and Chroma unavailable: {faiss_error}")
    
    elif backend == "chroma":
        _create_chroma_index(documents)
    else:
        raise ValueError(f"Unsupported vector database backend: {backend}")


def _load_vector_database():
    """Load the persisted vector database based on configured backend."""
    backend = getattr(config, "VECTOR_DB_BACKEND", "faiss").lower()
    
    if backend == "faiss":
        if not vector_db_exists():
            raise FileNotFoundError("FAISS index not found. Run create_vector_db() first.")
        
        return FAISS.load_local(
            config.VECTOR_DB_PATH,
            _get_embeddings(),
            allow_dangerous_deserialization=True,
        )
    
    elif backend == "chroma":
        if not HAS_CHROMA:
            raise RuntimeError("Chroma not available. Install with: pip install chromadb")
        
        return Chroma(
            embedding_function=_get_embeddings(),
            persist_directory=config.CHROMA_DB_PATH,
        )
    else:
        raise ValueError(f"Unsupported vector database backend: {backend}")


def _create_professional_prompt() -> PromptTemplate:
    """
    Create professional prompt template with LinkedIn integration.
    
    Engineered for interview-appropriate responses with proper guardrails
    against hallucination and clear instructions for professional tone.
    """
    linkedin_instruction = ""
    if hasattr(config, "LINKEDIN_URL") and config.LINKEDIN_URL:
        linkedin_instruction = (
            f"- When questions involve professional background, work history, or networking, "
            f"include Noah's LinkedIn profile: {config.LINKEDIN_URL}\n"
        )
    
    template = f"""Given the following context about Noah's professional background, provide a comprehensive, 
accurate response that demonstrates his qualifications and expertise.

INSTRUCTIONS:
- Use ONLY information from the provided context - never fabricate details
- Maintain a professional, interview-appropriate tone throughout
- Provide specific examples and concrete details when available
- If information isn't in the context, clearly state "This information isn't available in my current knowledge base"
{linkedin_instruction}
- Structure responses clearly with proper formatting

CONTEXT: {{context}}

QUESTION: {{question}}

PROFESSIONAL RESPONSE:"""
    
    return PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )


def get_qa_chain() -> RetrievalQA:
    """
    Create and return production-ready RetrievalQA chain.
    
    Features:
    - Optimized retriever with configurable similarity thresholds
    - Professional prompt engineering with LinkedIn integration
    - Source document return for transparency and verification
    - Enterprise-grade error handling and validation
    """
    # Load vector database
    vector_db = _load_vector_database()
    
    # Create retriever with optimized settings
    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": getattr(config, "RETRIEVER_TOP_K", 4),
            "score_threshold": config.RETRIEVER_SCORE_THRESHOLD
        }
    )
    
    # Create professional prompt
    prompt = _create_professional_prompt()
    
    # Build QA chain with enterprise configurations
    chain = RetrievalQA.from_chain_type(
        llm=_get_llm(),
        chain_type="stuff",
        retriever=retriever,
        input_key="query",
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    
    return chain


if __name__ == "__main__":
    """
    Development smoke test for system validation.
    Run this script directly to test the RAG pipeline.
    """
    print("🔧 Running RAG system validation...")
    
    try:
        # Test vector database creation
        print("📊 Creating vector database...")
        create_vector_db()
        print("✅ Vector database ready")
        
        # Test QA chain
        print("🔗 Initializing QA chain...")
        chain = get_qa_chain()
        print("✅ QA chain ready")
        
        # Test query processing
        print("🧪 Testing question processing...")
        test_query = "What is Noah's technical background?"
        result = chain.invoke({"query": test_query})
        
        answer = result.get("result", "No answer")
        sources = len(result.get("source_documents", []))
        
        print(f"✅ Test query successful!")
        print(f"📝 Answer preview: {answer[:100]}...")
        print(f"📚 Sources used: {sources}")
        print("\n🎉 RAG system validation completed successfully!")
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        raise