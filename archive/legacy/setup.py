#!/usr/bin/env python3
"""
Setup script for the Portfolio Q&A system.
Run this script to set up the environment and initialize the vector database.
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def check_env_file():
    """Check if .env file exists and has required variables."""
    env_path = Path('.env')
    if not env_path.exists():
        print("❌ .env file not found. Please copy .env.example to .env and fill in your API keys.")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
        if 'your_openai_api_key_here' in content:
            print("❌ Please update your .env file with your actual OpenAI API key.")
            return False
    
    print("✅ .env file found and configured")
    return True

def install_dependencies():
    """Install required Python packages."""
    print("📦 Installing dependencies...")
    os.system("pip install -r requirements.txt")
    print("✅ Dependencies installed")

def initialize_vector_db():
    """Initialize the vector database."""
    print("🔍 Initializing vector database...")
    try:
        from langchain_helper import create_vector_db
        create_vector_db()
        print("✅ Vector database initialized")
    except Exception as e:
        print(f"❌ Error initializing vector database: {e}")
        return False
    return True

def main():
    """Main setup function."""
    print("🚀 Portfolio Q&A Setup")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check environment file
    if not check_env_file():
        sys.exit(1)
    
    # Install dependencies
    install_dependencies()
    
    # Initialize vector database
    if not initialize_vector_db():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete! Your Portfolio Q&A system is ready to use.")
    print("\nNext steps:")
    print("1. Run 'python -m streamlit run main.py' to start the web interface")
    print("2. Or use the Jupyter notebook 'openai_codebasics_q_and_a.ipynb'")
    print("3. Or import langchain_helper in your Python scripts")

if __name__ == "__main__":
    main()