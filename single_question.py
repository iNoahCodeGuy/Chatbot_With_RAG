# Quick individual question tester - just change the question and run!
import sys, os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

# Setup
load_dotenv()
api_key = os.environ["OPENAI_API_KEY"]
llm = ChatOpenAI(model="gpt-4", temperature=0.1, openai_api_key=api_key)
loader = CSVLoader(file_path='noah_portfolio.csv', source_column="answer")
data = loader.load()
openai_embeddings = OpenAIEmbeddings(openai_api_key=api_key)
vectordb = FAISS.from_documents(documents=data, embedding=openai_embeddings)
retriever = vectordb.as_retriever(score_threshold=0.7)

prompt_template = """Given the following context and a question, generate an answer based on this context only.
In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

CONTEXT: {context}

QUESTION: {question}"""

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, input_key="query", return_source_documents=True, chain_type_kwargs={"prompt": PROMPT})

# CHANGE THIS QUESTION TO TEST DIFFERENT ONES:
question = "What is Noah's Education background?"

print(f"Question: {question}")
result = chain(question)
print(f"Answer: {result['result']}")
print(f"Sources: {len(result['source_documents'])}")