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

def create_vector_db() -> None:
    """Build and persist the FAISS index from the portfolio CSV.

    Reads the CSV configured in :class:`config`, embeds the configured column,
    and persists the FAISS index under :data:`vectordb_file_path`.
    """
    _ensure_config_valid()

    # Load Noah's professional portfolio data using configuration
    loader = CSVLoader(
        file_path=config.CSV_FILE_PATH,
        source_column=config.SOURCE_COLUMN,
    )
    data = loader.load()

    # Convert portfolio data into vectors for semantic search
    vectordb = FAISS.from_documents(
        documents=data,
        embedding=_get_embeddings(),  # Uses OpenAI embeddings to create embeddings
    )

    # Ensure the directory exists then save the vector database locally for quick access
    import os
    os.makedirs(vectordb_file_path, exist_ok=True)
    vectordb.save_local(vectordb_file_path)


def _build_prompt() -> PromptTemplate:
    """Return the prompt template for professional, context-grounded answers."""
    prompt_template = (
        "Given the following context about Noah's professional background and a question,\n"
        "provide a concise, professional response highlighting relevant skills, achievements, and experiences.\n\n"
        "Guidelines:\n"
        "- Be specific and pull concrete details from the context when available\n"
        "- Maintain a professional, interview-appropriate tone\n"
        "- If information is not in the context, acknowledge the limitation briefly\n\n"
        "CONTEXT: {context}\n\n"
        "QUESTION: {question}\n\n"
        "RESPONSE:"
    )
    return PromptTemplate(template=prompt_template, input_variables=["context", "question"])


def get_qa_chain() -> RetrievalQA:
    """Create and return the RetrievalQA chain using the persisted FAISS index."""
    # Load the vector database from the local folder
    vectordb = FAISS.load_local(
        vectordb_file_path,
        _get_embeddings(),
        allow_dangerous_deserialization=True,
    )

    # Create a retriever for querying the vector database using configuration
    retriever = vectordb.as_retriever(score_threshold=config.RETRIEVER_SCORE_THRESHOLD)
    PROMPT = _build_prompt()

    # Build the QA chain
    # - Uses the language model for generating responses
    # - Retrieves relevant context from Noah's portfolio
    # - Returns source documents for transparency
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
    print(chain("Tell me about Noah's sales experience"))