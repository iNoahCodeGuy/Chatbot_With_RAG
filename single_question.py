# Quick individual question tester - FAISS backend
import os, time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from config import config
from analytics import ChatbotAnalytics

load_dotenv()
llm = ChatOpenAI(model="gpt-4", temperature=0.1, api_key=os.environ.get("OPENAI_API_KEY"))
loader = CSVLoader(file_path=config.CSV_FILE_PATH, source_column=config.SOURCE_COLUMN)
docs = loader.load()
emb = OpenAIEmbeddings(model=config.OPENAI_EMBEDDING_MODEL, api_key=os.environ.get("OPENAI_API_KEY"))

vectordb = FAISS.from_documents(docs, embedding=emb)
retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k":4, "score_threshold":0.7})

prompt_template = """You are a professional assistant answering questions about Noah using ONLY the given context.
If context lacks the answer, say so briefly.
{linkedin}
CONTEXT: {{context}}

QUESTION: {{question}}

ANSWER:"""
linkedin = f"Include LinkedIn when relevant: {config.LINKEDIN_URL}" if config.LINKEDIN_URL else ""
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"], partial_variables={"linkedin": linkedin})

chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    input_key="query",
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)

question = "Walk me through Noah's career so far"
print(f"🤔 Question: {question}\n{'='*40}")
start = time.time()
result = chain.invoke({"query": question})
elapsed = (time.time() - start)*1000
answer = result.get('result','')
sources = result.get('source_documents', [])
print("Answer:\n", answer)
print(f"\nSources: {len(sources)} | Time: {elapsed:.1f}ms")

analytics = ChatbotAnalytics()
analytics.log_interaction(
    question=question,
    answer=answer,
    source_count=len(sources),
    response_time_ms=elapsed,
    linkedin_included=(config.LINKEDIN_URL in answer) if config.LINKEDIN_URL else False,
    is_career_related=True,
    session_id="single_question_test"
)
print("📊 Logged analytics.")