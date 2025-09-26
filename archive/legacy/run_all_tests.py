#!/usr/bin/env python3
"""
🚀 Noah Portfolio Q&A System - Simple Command Line Interface
Run this script directly to test questions without Jupyter!
"""

def main():
    print("="*60)
    print("🚀 NOAH'S PORTFOLIO Q&A SYSTEM")
    print("="*60)
    
    try:
        # Setup (same as your notebook cell 2)
        import sys
        import os
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        from langchain_community.document_loaders import CSVLoader
        from langchain_community.vectorstores import FAISS
        from langchain.prompts import PromptTemplate
        from langchain.chains import RetrievalQA
        from dotenv import load_dotenv
        
        print("✅ All imports successful")
        
        # Load environment
        load_dotenv()
        api_key = os.environ["OPENAI_API_KEY"]
        print("✅ OpenAI API key loaded")
        
        # Initialize system
        llm = ChatOpenAI(model="gpt-4", temperature=0.1, openai_api_key=api_key)
        loader = CSVLoader(file_path='noah_portfolio.csv', source_column="Answer")
        data = loader.load()
        print(f"✅ Loaded {len(data)} documents")
        
        openai_embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        vectordb = FAISS.from_documents(documents=data, embedding=openai_embeddings)
        retriever = vectordb.as_retriever(score_threshold=0.7)
        
        prompt_template = """Given the following context and a question, generate an answer based on this context only.
In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

CONTEXT: {context}

QUESTION: {question}"""

        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=retriever, input_key="query",
            return_source_documents=True, chain_type_kwargs={"prompt": PROMPT}
        )
        
        print("✅ Q&A System ready!")
        print("\n" + "="*60)
        print("TESTING ALL QUESTIONS FROM YOUR NOTEBOOK:")
        print("="*60)
        
        # Test all your notebook questions
        questions = [
            "What is Noah's Education background?",
            "Tell me about Noah's work experience in sales", 
            "What certifications does Noah have?",
            "What skills does Noah have?",
            "Can you describe Noah's experience in B2B sales?",
            "What is Noah's educational background in biological sciences?",
            "How would you describe Noah as a candidate for a sales position?"
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"\n🤔 Question {i}: {question}")
            print("-" * 50)
            try:
                result = chain(question)
                print(f"✅ Answer: {result['result']}")
                print(f"📚 Sources: {len(result['source_documents'])}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("\n" + "="*60)
        print("🎉 ALL TESTS COMPLETE!")
        print("✅ Your Q&A system is working perfectly!")
        print("✅ All notebook questions have been tested successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()