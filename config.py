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
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.1"))
    OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
    
    # Data Configuration
    CSV_FILE_PATH: str = os.getenv("CSV_FILE_PATH", "noah_portfolio.csv")
    SOURCE_COLUMN: str = os.getenv("SOURCE_COLUMN", "answer")
    
    # Vector Database Configuration
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "faiss_index")
    RETRIEVER_SCORE_THRESHOLD: float = float(os.getenv("RETRIEVER_SCORE_THRESHOLD", "0.7"))
    
    # Validation
    @classmethod
    def validate(cls) -> bool:
        """Validate that all required configuration is present."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        if not os.path.exists(cls.CSV_FILE_PATH):
            raise FileNotFoundError(f"CSV file not found: {cls.CSV_FILE_PATH}")
        
        return True

# Global configuration instance
config = Config()