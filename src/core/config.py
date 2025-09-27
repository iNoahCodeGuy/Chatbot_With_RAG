"""
Configuration Management
=======================

Centralized configuration with validation, type hints, and environment support.
Follows the principle of fail-fast with clear error messages.
"""

import os
from dataclasses import dataclass
from typing import Optional, Dict, Any
from pathlib import Path
import streamlit as st


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    faiss_index_path: str
    csv_data_path: str
    
    def __post_init__(self):
        """Validate paths exist."""
        if not Path(self.faiss_index_path).parent.exists():
            Path(self.faiss_index_path).parent.mkdir(parents=True, exist_ok=True)
        if not Path(self.csv_data_path).exists():
            raise FileNotFoundError(f"Knowledge base file not found: {self.csv_data_path}")


@dataclass 
class OpenAIConfig:
    """OpenAI API configuration."""
    api_key: str
    model: str = "gpt-4"
    embedding_model: str = "text-embedding-3-small"
    temperature: float = 0.1
    max_tokens: int = 1000
    
    def __post_init__(self):
        """Validate API key is present."""
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            raise ValueError("OpenAI API key must be configured")


@dataclass
class UIConfig:
    """UI-related configuration."""
    page_title: str = "Noah's AI Assistant"
    page_icon: str = "🤖"
    layout: str = "wide"
    sidebar_state: str = "expanded"


@dataclass
class AppConfig:
    """Main application configuration.
    
    This class serves as the central configuration hub, aggregating all
    configuration concerns and providing validation.
    """
    openai: OpenAIConfig
    database: DatabaseConfig  
    ui: UIConfig
    debug_mode: bool = False
    
    @classmethod
    def from_environment(cls) -> 'AppConfig':
        """Create configuration from environment variables and Streamlit secrets.
        
        Returns:
            AppConfig: Validated configuration instance
            
        Raises:
            ValueError: If required configuration is missing
            FileNotFoundError: If required files don't exist
        """
        # Get OpenAI API key from multiple sources (Streamlit secrets, env vars)
        api_key = None
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except (KeyError, FileNotFoundError):
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError(
                "OpenAI API key not found. Please set it in .streamlit/secrets.toml "
                "or as an environment variable OPENAI_API_KEY"
            )
        
        # Build configuration
        return cls(
            openai=OpenAIConfig(api_key=api_key),
            database=DatabaseConfig(
                faiss_index_path="faiss_index/index.faiss",
                csv_data_path="noah_portfolio.csv"
            ),
            ui=UIConfig(),
            debug_mode=os.getenv("DEBUG", "false").lower() == "true"
        )


# Global configuration instance (singleton pattern)
_config_instance: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Get the global configuration instance.
    
    Implements singleton pattern to ensure consistent configuration
    across the application.
    
    Returns:
        AppConfig: The global configuration instance
    """
    global _config_instance
    
    if _config_instance is None:
        _config_instance = AppConfig.from_environment()
    
    return _config_instance


def reload_config() -> AppConfig:
    """Force reload of configuration (useful for testing).
    
    Returns:
        AppConfig: Newly loaded configuration instance
    """
    global _config_instance
    _config_instance = None
    return get_config()