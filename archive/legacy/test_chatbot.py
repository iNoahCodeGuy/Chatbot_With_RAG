"""
Quick test script to verify the Q&A system is working
"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

def test_chatbot():
    print("🧪 Testing Noah's Portfolio Chatbot...")
    print("="*50)
    
    # Load environment and setup
    load_dotenv()
    api_key = os.environ["OPENAI_API_KEY"]
    
    # Initialize components
    llm = ChatOpenAI(model="gpt-4", temperature=0.1, openai_api_key=api_key)
    loader = CSVLoader(file_path='noah_portfolio.csv', source_column="Answer")
    data = loader.load()
    openai_embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vectordb = FAISS.from_documents(documents=data, embedding=openai_embeddings)
    retriever = vectordb.as_retriever(score_threshold=0.7)
    
    # Create Q&A chain
    prompt_template = """Given the following context and a question, generate an answer based on this context only.
In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

CONTEXT: {context}

QUESTION: {question}"""

    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain_type_kwargs = {"prompt": PROMPT}
    
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        input_key="query",
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs
    )
    
    # Test questions
    questions = [
        "What is Noah's Education background?",
        "Tell me about Noah's work experience in sales",
        "What certifications does Noah have?",
        "What skills does Noah have?",
        "Can you describe Noah's experience in B2B sales?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n❓ Question {i}: {question}")
        print("-" * 40)
        try:
            result = chain(question)
            print(f"✅ Answer: {result['result']}")
            print(f"📚 Sources: {len(result['source_documents'])}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    test_chatbot()