"""
Configuration management for the Portfolio Q&A system.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Portfolio Q&A system."""
    
    # Try to get from Streamlit secrets first, then environment variables
    def _get_secret(self, key: str, default: str = "") -> str:
        """Get secret from Streamlit secrets or environment variables."""
        try:
            # Try Streamlit secrets first
            import streamlit as st
            if hasattr(st, 'secrets') and key in st.secrets:
                return st.secrets[key]
        except:
            pass
        # Fall back to environment variables
        return os.getenv(key, default)
    
    @property
    def OPENAI_API_KEY(self) -> str:
        return self._get_secret("OPENAI_API_KEY")
    
    # OpenAI Configuration
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.1"))
    # Default to modern embedding model; override via env/Secrets if needed
    OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    
    # Data Configuration
    CSV_FILE_PATH: str = os.getenv("CSV_FILE_PATH", "noah_portfolio.csv")
    SOURCE_COLUMN: str = os.getenv("SOURCE_COLUMN", "answer")
    
    # Vector Database Configuration
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "faiss_index")
    RETRIEVER_SCORE_THRESHOLD: float = float(os.getenv("RETRIEVER_SCORE_THRESHOLD", "0.7"))
    
    # Validation
    def validate(self) -> bool:
        """Validate that all required configuration is present."""
        api_key = self.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required. Set it in .env file or Streamlit secrets.")
        
        if not os.path.exists(self.CSV_FILE_PATH):
            raise FileNotFoundError(f"CSV file not found: {self.CSV_FILE_PATH}")
        
        return True

# Global configuration instance
config = Config()