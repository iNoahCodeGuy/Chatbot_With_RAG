"""
LangChain Helper Utilities (FAISS Version)
=========================================

Production-quality RAG utilities with explicit FAISS vector store.
Readable for juniors; robust for production.

Key Patterns:
- Lazy singleton resources (LLM + Embeddings)
- Deterministic prompt with LinkedIn injection
- Explicit index build / load separation
- Clear error surfacing for faster debugging
"""

import os
from typing import Optional
from pathlib import Path

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from config import config

_llm_instance: Optional[ChatOpenAI] = None
_embeddings_instance: Optional[OpenAIEmbeddings] = None

INDEX_DIR = Path(config.VECTOR_DB_PATH)
FAISS_INDEX_FILE = INDEX_DIR / "index.faiss"
FAISS_STORE_FILE = INDEX_DIR / "index.pkl"

# ---------------- Core Resource Accessors ---------------- #

def _ensure_config_valid() -> None:
    config.validate()


def _get_llm() -> ChatOpenAI:
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
    global _embeddings_instance
    if _embeddings_instance is None:
        _ensure_config_valid()
        _embeddings_instance = OpenAIEmbeddings(
            model=config.OPENAI_EMBEDDING_MODEL,
            api_key=config.OPENAI_API_KEY,
        )
    return _embeddings_instance

# ---------------- Data Loading & Vector Store ---------------- #

def _load_portfolio_documents():
    if not os.path.exists(config.CSV_FILE_PATH):
        raise FileNotFoundError(f"Portfolio CSV not found: {config.CSV_FILE_PATH}")
    loader = CSVLoader(file_path=config.CSV_FILE_PATH, source_column=config.SOURCE_COLUMN)
    docs = loader.load()
    if not docs:
        raise ValueError("No documents loaded from CSV file")
    return docs


def vector_db_exists() -> bool:
    return FAISS_INDEX_FILE.exists() and FAISS_STORE_FILE.exists()


def create_vector_db() -> None:
    """Build and persist FAISS index from portfolio CSV."""
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    docs = _load_portfolio_documents()
    vectordb = FAISS.from_documents(docs, embedding=_get_embeddings())
    vectordb.save_local(str(INDEX_DIR))


def _load_vector_db() -> FAISS:
    if not vector_db_exists():
        raise FileNotFoundError("FAISS index missing. Run create_vector_db() first.")
    return FAISS.load_local(
        str(INDEX_DIR),
        _get_embeddings(),
        allow_dangerous_deserialization=True,  # needed for current langchain serialization format
    )

# ---------------- Prompt Engineering ---------------- #

def _build_prompt() -> PromptTemplate:
    linkedin_line = ""
    if getattr(config, "LINKEDIN_URL", ""):
        linkedin_line = f"- For career/history questions include LinkedIn: {config.LINKEDIN_URL}\n"
    template = f"""You are a professional assistant answering questions about Noah.
Use ONLY the provided context. If the answer isn't present, say you don't have that information.
Be concise, factual, and professional.
{linkedin_line}
CONTEXT: {{context}}

QUESTION: {{question}}

ANSWER:"""
    return PromptTemplate(template=template, input_variables=["context", "question"])

# ---------------- Public Chain Factory ---------------- #

def get_qa_chain() -> RetrievalQA:
    vectordb = _load_vector_db()
    retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": getattr(config, "RETRIEVER_TOP_K", 4),
            "score_threshold": config.RETRIEVER_SCORE_THRESHOLD,
        },
    )
    prompt = _build_prompt()
    return RetrievalQA.from_chain_type(
        llm=_get_llm(),
        chain_type="stuff",
        retriever=retriever,
        input_key="query",
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )

# ---------------- CLI Validation ---------------- #
if __name__ == "__main__":
    print("🔧 Validating FAISS RAG pipeline...")
    try:
        if not vector_db_exists():
            print("📦 Building FAISS index...")
            create_vector_db()
            print("✅ Index built")
        print("⚙️  Initializing QA chain...")
        chain = get_qa_chain()
        print("🧪 Running test query...")
        result = chain.invoke({"query": "What technical skills does Noah have?"})
        ans = result.get("result", "(no answer)")
        print("✅ Success. Answer preview:", ans[:120], "...")
        print("📚 Sources:", len(result.get("source_documents", [])))
        print("🎉 Validation complete")
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        raise