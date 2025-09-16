# Test script for Noah's portfolio Q&A functionality

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.environ["OPENAI_API_KEY"]

print("1. Initializing OpenAI models...")
# Initialize GPT-4 model
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.1,
    openai_api_key=api_key
)

# Initialize OpenAI embeddings
openai_embeddings = OpenAIEmbeddings(openai_api_key=api_key)
print("✅ OpenAI models initialized")

print("\n2. Loading Noah's portfolio data...")
# Load Noah's portfolio CSV
loader = CSVLoader(file_path='noah_portfolio.csv', source_column="answer")
data = loader.load()
print(f"✅ Loaded {len(data)} documents about Noah's background")

print("\n3. Testing embeddings...")
# Test embedding
e = openai_embeddings.embed_query("What is Noah's Professional Background?")
print(f"✅ Embedding created with {len(e)} dimensions")
print(f"First 5 values: {e[:5]}")

print("\n4. Creating vector database...")
# Create FAISS vector database
vectordb = FAISS.from_documents(documents=data, embedding=openai_embeddings)
retriever = vectordb.as_retriever(score_threshold=0.7)
print("✅ FAISS vector database created")

print("\n5. Testing document retrieval...")
# Test retrieval
rdocs = retriever.get_relevant_documents("What is Noah's professional background?")
print(f"✅ Retrieved {len(rdocs)} relevant documents")
for i, doc in enumerate(rdocs):
    print(f"Document {i+1}: {doc.page_content[:100]}...")

print("\n6. Creating Q&A chain...")
# Create prompt template
prompt_template = """Given the following context and a question, generate an answer based on this context only.
In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

CONTEXT: {context}

QUESTION: {question}"""

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs = {"prompt": PROMPT}

# Create RetrievalQA chain
chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    input_key="query",
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)
print("✅ Q&A chain created successfully")

print("\n7. Testing the complete system...")
# Test the complete system
result = chain("What is Noah's Professional Background?")
print("\n🎉 SYSTEM TEST SUCCESSFUL!")
print("\n" + "="*50)
print("QUESTION: What is Noah's Professional Background?")
print("="*50)
print("ANSWER:")
print(result['result'])
print("\n" + "="*50)

print("\n✅ All components are working correctly!")
print("The portfolio Q&A system is ready to use!")