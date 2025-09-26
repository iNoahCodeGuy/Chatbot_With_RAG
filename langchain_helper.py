"""LangChain helper utilities with lazy initialization.

Purpose
-------
Avoid heavy work at import time so the Streamlit app can start even if secrets
or files are missing. Initialize models and stores only when the public
functions are called, and raise informative errors.
"""

from typing import Optional

# Import required LangChain components
from langchain_community.vectorstores import FAISS  # Vector database for storing and searching embeddings
from langchain_openai import ChatOpenAI  # OpenAI's chat model interface
from langchain_community.document_loaders.csv_loader import CSVLoader  # For loading CSV portfolio data
from langchain_openai import OpenAIEmbeddings  # For creating text embeddings
from langchain.prompts import PromptTemplate  # For creating custom prompt templates
from langchain.chains import RetrievalQA  # For building Q&A chain
from config import config  # Import centralized configuration

# Optional Chroma fallback
try:
    from langchain_community.vectorstores import Chroma  # type: ignore
    _has_chroma = True
except Exception:
    _has_chroma = False

_llm: Optional[ChatOpenAI] = None
_embeddings: Optional[OpenAIEmbeddings] = None

def _ensure_config_valid() -> None:
    """Validate configuration lazily with clearer error messages."""
    try:
        config.validate()
    except Exception as e:
        raise RuntimeError(f"Configuration error: {e}")

def _get_llm() -> ChatOpenAI:
    global _llm
    if _llm is None:
        _ensure_config_valid()
        _llm = ChatOpenAI(
            model=config.OPENAI_MODEL,
            temperature=config.OPENAI_TEMPERATURE,
            api_key=config.OPENAI_API_KEY,
        )
    return _llm

def _get_embeddings() -> OpenAIEmbeddings:
    global _embeddings
    if _embeddings is None:
        _ensure_config_valid()
        try:
            _embeddings = OpenAIEmbeddings(
                model=config.OPENAI_EMBEDDING_MODEL,
                api_key=config.OPENAI_API_KEY,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize OpenAI embeddings: {e}")
    return _embeddings

# Path where the vector database will be saved
vectordb_file_path = config.VECTOR_DB_PATH

def vector_db_exists() -> bool:
    """Return True if the FAISS index files exist on disk."""
    import os
    idx_dir = vectordb_file_path
    faiss_path = os.path.join(idx_dir, "index.faiss")
    pkl_path = os.path.join(idx_dir, "index.pkl")
    return os.path.exists(faiss_path) and os.path.exists(pkl_path)

def _load_csv_documents():
    loader = CSVLoader(
        file_path=config.CSV_FILE_PATH,
        source_column=config.SOURCE_COLUMN,
    )
    return loader.load()

def _build_with_faiss(data):
    vectordb = FAISS.from_documents(
        documents=data,
        embedding=_get_embeddings(),
    )
    import os
    os.makedirs(vectordb_file_path, exist_ok=True)
    vectordb.save_local(vectordb_file_path)
    return vectordb

def _build_with_chroma(data):
    if not _has_chroma:
        raise RuntimeError("Chroma vector store not available and FAISS failed. Install chromadb or fix faiss-cpu.")
    import os
    os.makedirs(config.CHROMA_DB_PATH, exist_ok=True)
    vectordb = Chroma.from_documents(
        documents=data,
        embedding=_get_embeddings(),
        persist_directory=config.CHROMA_DB_PATH,
    )
    vectordb.persist()
    return vectordb

def create_vector_db() -> None:
    """Build and persist the vector index from the portfolio CSV using the selected backend."""
    _ensure_config_valid()
    data = _load_csv_documents()

    backend = (getattr(config, "VECTOR_DB_BACKEND", "faiss") or "faiss").lower()
    if backend == "faiss":
        try:
            _build_with_faiss(data)
            return
        except Exception as e:
            # Fallback to Chroma if FAISS isn't available
            if _has_chroma:
                _build_with_chroma(data)
                return
            raise
    elif backend == "chroma":
        _build_with_chroma(data)
        return
    else:
        raise ValueError(f"Unsupported VECTOR_DB_BACKEND: {backend}")

def _load_vectordb():
    backend = (getattr(config, "VECTOR_DB_BACKEND", "faiss") or "faiss").lower()
    if backend == "faiss":
        return FAISS.load_local(
            vectordb_file_path,
            _get_embeddings(),
            allow_dangerous_deserialization=True,
        )
    elif backend == "chroma":
        if not _has_chroma:
            raise RuntimeError("Chroma vector store not available. Install chromadb.")
        return Chroma(
            embedding_function=_get_embeddings(),
            persist_directory=config.CHROMA_DB_PATH,
        )
    else:
        raise ValueError(f"Unsupported VECTOR_DB_BACKEND: {backend}")

def _build_prompt() -> PromptTemplate:
    """Return the prompt template for professional, context-grounded answers with guardrails and citation."""
    linkedin_hint = ""
    try:
        if getattr(config, "LINKEDIN_URL", ""):
            linkedin_hint = f"- When the question asks about roles, work history, or how to connect, include Noah's LinkedIn URL: {config.LINKEDIN_URL}\n"
    except Exception:
        pass

    prompt_template = (
        "Given the following context about Noah's professional background and a question,\n"
        "provide a concise, professional response highlighting relevant skills, achievements, and experiences.\n\n"
        "Guidelines:\n"
        "- Be specific and pull concrete details from the context when available\n"
        "- Maintain a professional, interview-appropriate tone\n"
        "- If information is not in the context, briefly say you don't know rather than inventing details\n"
        f"{linkedin_hint}"
        "\nCONTEXT: {context}\n\n"
        "QUESTION: {question}\n\n"
        "RESPONSE:"
    )
    return PromptTemplate(template=prompt_template, input_variables=["context", "question"])

def get_qa_chain() -> RetrievalQA:
    """Create and return the RetrievalQA chain using the persisted vector index."""
    # Load the vector database from the local folder or Chroma
    vectordb = _load_vectordb()

    # Create a retriever for querying the vector database using configuration
    retriever = vectordb.as_retriever(score_threshold=config.RETRIEVER_SCORE_THRESHOLD)
    PROMPT = _build_prompt()

    # Build the QA chain
    chain = RetrievalQA.from_chain_type(
        llm=_get_llm(),
        chain_type="stuff",
        retriever=retriever,
        input_key="query",
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )

    return chain

if __name__ == "__main__":
    # Simple manual smoke test
    create_vector_db()
    chain = get_qa_chain()
    print(chain.invoke({"query": "Tell me about Noah's sales experience"}))  # Updated to use invoke()