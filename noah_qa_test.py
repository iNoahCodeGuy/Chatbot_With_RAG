#!/usr/bin/env python3
"""
🚀 Noah Portfolio Q&A System - Interactive Test Script
This script bypasses all Jupyter kernel issues and runs directly with Python 3.13
"""

import sys
import os
from dotenv import load_dotenv

def main():
    print("🚀 Noah's Portfolio Q&A System - Interactive Testing")
    print("="*60)
    
    # Check Python version
    print(f"✅ Python version: {sys.version.split()[0]}")
    print(f"✅ Executable: {sys.executable}")
    
    if "Python313" in sys.executable:
        print("✅ Using correct Python 3.13 installation")
    elif "WindowsApps" in sys.executable:
        print("⚠️  WARNING: Using Windows Store Python - this may cause issues!")
    
    try:
        # Load environment variables
        load_dotenv()
        api_key = os.environ.get("OPENAI_API_KEY")
        
        if not api_key or not api_key.startswith('sk-'):
            print("❌ OpenAI API key not found or invalid!")
            print("   Make sure your .env file contains: OPENAI_API_KEY=sk-your-key-here")
            return
        
        print("✅ OpenAI API key loaded")
        
        # Import all required packages
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        from langchain_community.document_loaders import CSVLoader
        from langchain_community.vectorstores import FAISS
        from langchain.prompts import PromptTemplate
        from langchain.chains import RetrievalQA
        print("✅ All imports successful")
        
        # Step 1: Initialize LLM
        llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            openai_api_key=api_key
        )
        print("✅ Step 1: LLM initialized")
        
        # Step 2: Load CSV data
        if not os.path.exists('noah_portfolio.csv'):
            print("❌ noah_portfolio.csv not found!")
            return
            
        loader = CSVLoader(file_path='noah_portfolio.csv', source_column="answer")
        data = loader.load()
        print(f"✅ Step 2: Loaded {len(data)} documents")
        
        # Step 3: Create embeddings
        openai_embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        print("✅ Step 3: Embeddings initialized")
        
        # Step 4: Create vector database
        print("   Creating vector database... (may take a moment)")
        vectordb = FAISS.from_documents(documents=data, embedding=openai_embeddings)
        retriever = vectordb.as_retriever(score_threshold=0.7)
        print("✅ Step 4: Vector database created")
        
        # Step 5: Create Q&A chain
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
        
        print("\n🎉 SUCCESS! Noah's Q&A System is ready!")
        print("="*60)
        
        # Interactive Q&A loop
        print("\n🧪 INTERACTIVE Q&A SESSION")
        print("Ask questions about Noah's background, or type 'quit' to exit")
        print("Sample questions:")
        print("- What is Noah's education background?")
        print("- Tell me about Noah's work experience in sales")
        print("- What certifications does Noah have?")
        print("- What skills does Noah have?")
        print("- Can you describe Noah's experience in B2B sales?")
        print("-" * 60)
        
        while True:
            try:
                question = input("\n🤔 Your question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not question:
                    continue
                
                print("\n🔍 Searching for answer...")
                result = chain(question)
                
                print(f"\n🎯 Answer:")
                print(f"{result['result']}")
                print(f"\n📚 Sources used: {len(result['source_documents'])}")
                print("-" * 60)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error processing question: {e}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n🔧 To fix, run in terminal:")
        print("C:\\Users\\ndelacalzada\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m pip install langchain-openai langchain-community faiss-cpu python-dotenv")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()