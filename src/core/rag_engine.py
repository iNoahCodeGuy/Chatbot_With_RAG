"""
RAG (Retrieval-Augmented Generation) Engine
==========================================

Core RAG functionality with clean interfaces and proper error handling.
Follows dependency injection and single responsibility principles.
"""

import streamlit as st
from typing import Optional, Dict, Any, List
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.schema import Document
from pathlib import Path
import logging

from .config import AppConfig


logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Handles document loading and processing for the knowledge base.
    
    Separates document processing concerns from the main RAG engine,
    making it easier to test and maintain.
    """
    
    def __init__(self, csv_path: str):
        """Initialize document processor.
        
        Args:
            csv_path: Path to the CSV knowledge base file
        """
        self.csv_path = csv_path
    
    def load_documents(self) -> List[Document]:
        """Load and process documents from CSV.
        
        Returns:
            List[Document]: Processed documents ready for embedding
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If CSV format is invalid
        """
        if not Path(self.csv_path).exists():
            raise FileNotFoundError(f"Knowledge base file not found: {self.csv_path}")
        
        try:
            # Load CSV with proper configuration
            loader = CSVLoader(
                file_path=self.csv_path,
                encoding="utf-8"
            )
            documents = loader.load()
            
            if not documents:
                raise ValueError("No documents loaded from CSV file")
            
            logger.info(f"Loaded {len(documents)} documents from {self.csv_path}")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading documents: {str(e)}")
            raise ValueError(f"Failed to load knowledge base: {str(e)}")


class VectorStore:
    """Manages the vector database for document embeddings.
    
    Handles FAISS vector store creation, loading, and saving with
    proper error handling and caching.
    """
    
    def __init__(self, embeddings: OpenAIEmbeddings, index_path: str):
        """Initialize vector store manager.
        
        Args:
            embeddings: OpenAI embeddings instance
            index_path: Path to FAISS index file
        """
        self.embeddings = embeddings
        self.index_path = index_path
        self._vector_store: Optional[FAISS] = None
    
    def get_or_create_vector_store(self, documents: List[Document]) -> FAISS:
        """Get existing vector store or create new one from documents.
        
        Args:
            documents: Documents to create vector store from if not exists
            
        Returns:
            FAISS: Vector store instance
        """
        if self._vector_store is not None:
            return self._vector_store
        
        # Try to load existing vector store
        if Path(self.index_path).exists():
            try:
                self._vector_store = FAISS.load_local(
                    Path(self.index_path).parent.as_posix(),
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info(f"Loaded existing vector store from {self.index_path}")
                return self._vector_store
            except Exception as e:
                logger.warning(f"Failed to load existing vector store: {e}")
        
        # Create new vector store
        return self._create_new_vector_store(documents)
    
    def _create_new_vector_store(self, documents: List[Document]) -> FAISS:
        """Create and save new vector store from documents.
        
        Args:
            documents: Documents to create embeddings from
            
        Returns:
            FAISS: New vector store instance
        """
        logger.info("Creating new vector store from documents...")
        
        try:
            self._vector_store = FAISS.from_documents(documents, self.embeddings)
            
            # Save to disk
            index_dir = Path(self.index_path).parent
            index_dir.mkdir(parents=True, exist_ok=True)
            self._vector_store.save_local(index_dir.as_posix())
            
            logger.info(f"Created and saved new vector store to {self.index_path}")
            return self._vector_store
            
        except Exception as e:
            logger.error(f"Failed to create vector store: {e}")
            raise RuntimeError(f"Vector store creation failed: {str(e)}")


class RAGEngine:
    """Main RAG engine orchestrating document retrieval and generation.
    
    This class follows the facade pattern, providing a clean interface
    to the complex RAG functionality while maintaining separation of concerns.
    """
    
    def __init__(self, config: AppConfig):
        """Initialize RAG engine with configuration.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self._llm: Optional[OpenAI] = None
        self._embeddings: Optional[OpenAIEmbeddings] = None
        self._qa_chain: Optional[RetrievalQA] = None
        
        # Initialize components
        self.doc_processor = DocumentProcessor(config.database.csv_data_path)
        self._vector_store_manager: Optional[VectorStore] = None
    
    @property
    def llm(self) -> OpenAI:
        """Get or create LLM instance (lazy initialization).
        
        Returns:
            OpenAI: LLM instance
        """
        if self._llm is None:
            self._llm = OpenAI(
                openai_api_key=self.config.openai.api_key,
                model_name=self.config.openai.model,
                temperature=self.config.openai.temperature,
                max_tokens=self.config.openai.max_tokens
            )
        return self._llm
    
    @property
    def embeddings(self) -> OpenAIEmbeddings:
        """Get or create embeddings instance (lazy initialization).
        
        Returns:
            OpenAIEmbeddings: Embeddings instance
        """
        if self._embeddings is None:
            self._embeddings = OpenAIEmbeddings(
                openai_api_key=self.config.openai.api_key,
                model=self.config.openai.embedding_model
            )
        return self._embeddings
    
    @property 
    def vector_store_manager(self) -> VectorStore:
        """Get or create vector store manager (lazy initialization).
        
        Returns:
            VectorStore: Vector store manager instance
        """
        if self._vector_store_manager is None:
            self._vector_store_manager = VectorStore(
                self.embeddings, 
                self.config.database.faiss_index_path
            )
        return self._vector_store_manager
    
    def get_qa_chain(self) -> RetrievalQA:
        """Get or create QA chain (lazy initialization with caching).
        
        Returns:
            RetrievalQA: Question-answering chain
            
        Raises:
            RuntimeError: If chain creation fails
        """
        if self._qa_chain is not None:
            return self._qa_chain
        
        try:
            # Load documents and create vector store
            documents = self.doc_processor.load_documents()
            vector_store = self.vector_store_manager.get_or_create_vector_store(documents)
            
            # Create QA chain
            self._qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=vector_store.as_retriever(search_kwargs={"k": 4}),
                return_source_documents=True
            )
            
            logger.info("QA chain created successfully")
            return self._qa_chain
            
        except Exception as e:
            logger.error(f"Failed to create QA chain: {e}")
            raise RuntimeError(f"RAG engine initialization failed: {str(e)}")
    
    def query(self, question: str) -> Dict[str, Any]:
        """Process a question and return answer with sources.
        
        Args:
            question: User's question
            
        Returns:
            Dict[str, Any]: Answer and source documents
            
        Raises:
            ValueError: If question is empty
            RuntimeError: If query processing fails
        """
        if not question.strip():
            raise ValueError("Question cannot be empty")
        
        try:
            qa_chain = self.get_qa_chain()
            result = qa_chain({"query": question})
            
            return {
                "answer": result["result"],
                "sources": result.get("source_documents", []),
                "question": question
            }
            
        except Exception as e:
            logger.error(f"Query processing failed: {e}")
            raise RuntimeError(f"Failed to process question: {str(e)}")


# Streamlit cached instance for performance
@st.cache_resource(show_spinner=False)
def get_rag_engine(config: AppConfig) -> RAGEngine:
    """Get cached RAG engine instance.
    
    Args:
        config: Application configuration
        
    Returns:
        RAGEngine: Cached RAG engine instance
    """
    return RAGEngine(config)