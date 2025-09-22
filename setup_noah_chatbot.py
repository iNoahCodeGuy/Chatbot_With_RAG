"""
Noah's Portfolio Q&A Setup Script
Run this script to set up the complete chatbot system
"""

import sys
import os
from pathlib import Path

def main():
    print("🚀 Setting up Noah's Portfolio Q&A System...")
    print("=" * 60)
    
    # System diagnostics
    print("🔍 System Diagnostics:")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current directory: {os.getcwd()}")
    
    # Check if we're using the correct Python installation
    if "WindowsApps" in sys.executable:
        print("⚠️  WARNING: You're using Windows Store Python!")
        print("   This version may have package installation issues.")
        return False
    elif "Python313" in sys.executable or "python313" in sys.executable.lower():
        print("✅ Using correct Python 3.13 installation")
    else:
        print(f"ℹ️  Using Python from: {sys.executable}")

    print("\n📦 Checking packages...")
    
    try:
        # Check all imports
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        from langchain.document_loaders.csv_loader import CSVLoader
        from langchain.vectorstores import FAISS
        from langchain.prompts import PromptTemplate
        from langchain.chains import RetrievalQA
        from dotenv import load_dotenv
        print("✅ All LangChain imports successful")
        
        # Load environment variables
        load_dotenv()
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key and api_key.startswith('sk-'):
            print("✅ OpenAI API key loaded and valid format")
            
            # Test a simple API call
            try:
                llm = ChatOpenAI(model="gpt-4", temperature=0.1, openai_api_key=api_key)
                print("✅ OpenAI API connection successful")
            except Exception as api_error:
                print(f"❌ OpenAI API test failed: {api_error}")
                return False
        else:
            print("❌ OpenAI API key not found or invalid format")
            print("Please make sure your .env file contains: OPENAI_API_KEY=sk-...")
            return False
            
        # Check CSV file
        if os.path.exists('noah_portfolio.csv'):
            print("✅ noah_portfolio.csv found")
            # Check CSV content
            with open('noah_portfolio.csv', 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"   CSV has {len(lines)} lines")
        else:
            print("❌ noah_portfolio.csv not found in current directory")
            csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
            if csv_files:
                print(f"Available CSV files: {csv_files}")
            else:
                print("No CSV files found")
            return False
            
        print("\n🔧 Setting up the Q&A system...")
        
        # Initialize LLM
        llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            openai_api_key=api_key
        )
        print("✅ Step 1: LLM initialized")
        
        # Load data
        loader = CSVLoader(file_path='noah_portfolio.csv', source_column="answer")
        data = loader.load()
        print(f"✅ Step 2: Loaded {len(data)} documents")
        
        # Create embeddings
        openai_embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        print("✅ Step 3: Embeddings initialized")
        
        # Create vector database
        print("   Creating vector database... (this may take a moment)")
        vectordb = FAISS.from_documents(documents=data, embedding=openai_embeddings)
        retriever = vectordb.as_retriever(score_threshold=0.7)
        print("✅ Step 4: Vector database created")
        
        # Create Q&A chain
        prompt_template = """Given the following context and a question, generate an answer based on this context only.
In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

CONTEXT: {context}

QUESTION: {question}"""

        PROMPT = PromptTemplate(
            template=prompt_template, 
            input_variables=["context", "question"]
        )
        
        chain_type_kwargs = {"prompt": PROMPT}
        
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            input_key="query",
            return_source_documents=True,
            chain_type_kwargs=chain_type_kwargs
        )
        print("✅ Step 5: Q&A chain created")
        
        # Test the system
        print("\n🧪 Testing the Q&A system...")
        test_result = chain("What is Noah's Professional Background?")
        
        print("\n🎯 Test Result:")
        print("Question: What is Noah's Professional Background?")
        print(f"Answer: {test_result['result']}")
        print(f"Sources used: {len(test_result['source_documents'])}")
        
        # Save the FAISS index for future use
        if not os.path.exists('faiss_index'):
            print("\n💾 Saving FAISS index...")
            vectordb.save_local("faiss_index")
            print("✅ FAISS index saved to 'faiss_index' directory")
        
        print("\n🎉 SUCCESS! Noah's Portfolio Q&A System is ready!")
        print("="*60)
        print("You can now:")
        print("1. Use the Flask web app (run: python app.py)")
        print("2. Test individual questions in the Jupyter notebook")
        print("3. Ask questions about Noah's background")
        print("="*60)
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n🔧 Fix by running in terminal:")
        print("pip install langchain-openai langchain-community faiss-cpu python-dotenv")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✨ Setup completed successfully! ✨")
    else:
        print("\n❌ Setup failed. Please fix the issues above and try again.")