"""
Configuration management for the Portfolio Q&A system.
"""
import os
from typing import Optional

# Make dotenv optional for resilience
try:
    from dotenv import load_dotenv  # type: ignore
except Exception:  # pragma: no cover - fallback when python-dotenv isn't available
    def load_dotenv(*args, **kwargs):  # type: ignore
        return False

# Load environment variables (no-op if load_dotenv is fallback)
load_dotenv()

class Config:
    """Configuration class for the Portfolio Q&A system."""
    
    # Try to get from Streamlit secrets first, then environment variables
    def _get_secret(self, key: str, default: str = "") -> str:
        """Get secret from Streamlit secrets, environment variables, or .streamlit/secrets.toml fallback."""
        try:
            # Try Streamlit secrets first
            import streamlit as st
            if hasattr(st, 'secrets') and key in st.secrets:
                return st.secrets[key]
        except Exception:
            pass
        # Fall back to environment variables
        val = os.getenv(key)
        if val:
            return val
        # Final fallback: read from .streamlit/secrets.toml if available (works outside Streamlit)
        try:
            import os as _os
            import tomllib as _tomllib  # Python 3.11+
            base_dir = _os.path.dirname(__file__)
            secrets_path = _os.path.join(base_dir, ".streamlit", "secrets.toml")
            if _os.path.exists(secrets_path):
                with open(secrets_path, "rb") as f:
                    data = _tomllib.load(f)
                if key in data:
                    return data.get(key, default)
        except Exception:
            pass
        return default
    
    @property
    def OPENAI_API_KEY(self) -> str:
        return self._get_secret("OPENAI_API_KEY")
    
    # OpenAI Configuration
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.1"))
    # Default to modern embedding model; override via env/Secrets if needed
    OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    
    # Data Configuration (readable from secrets/env with safe defaults)
    @property
    def CSV_FILE_PATH(self) -> str:
        # allow override via Streamlit secrets or env; default remains legacy file until new KB is provided
        return self._get_secret("CSV_FILE_PATH", os.getenv("CSV_FILE_PATH", "noah_portfolio.csv"))
    
    @property
    def SOURCE_COLUMN(self) -> str:
        # enforce capital-A default, but allow override
        return self._get_secret("SOURCE_COLUMN", os.getenv("SOURCE_COLUMN", "Answer"))
    
    @property
    def LINKEDIN_URL(self) -> str:
        """Optional LinkedIn URL for UI surfacing when relevant."""
        return self._get_secret("LINKEDIN_URL", os.getenv("LINKEDIN_URL", ""))
    
    # Vector Database Configuration (FAISS default)
    VECTOR_DB_BACKEND: str = os.getenv("VECTOR_DB_BACKEND", "faiss")  # only 'faiss' supported now
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "faiss_index")  # directory for faiss index files
    RETRIEVER_SCORE_THRESHOLD: float = float(os.getenv("RETRIEVER_SCORE_THRESHOLD", "0.7"))
    
    # Validation
    def validate(self) -> bool:
        """Validate that all required configuration is present."""
        api_key = self.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required. Set it in .env file, Streamlit secrets, or .streamlit/secrets.toml.")
        
        if not os.path.exists(self.CSV_FILE_PATH):
            raise FileNotFoundError(f"CSV file not found: {self.CSV_FILE_PATH}")
        
        return True

# Global configuration instance
config = Config()