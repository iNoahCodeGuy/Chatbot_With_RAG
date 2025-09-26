# Quick individual question tester - just change the question and run!
import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from config import config
from analytics import ChatbotAnalytics

# Setup
load_dotenv()
llm = ChatOpenAI(model="gpt-4", temperature=0.1, openai_api_key=os.environ["OPENAI_API_KEY"])
loader = CSVLoader(file_path='noah_portfolio.csv', source_column="Answer")
data = loader.load()
embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
vectordb = FAISS.from_documents(documents=data, embedding=embeddings)
retriever = vectordb.as_retriever(score_threshold=0.7)
analytics = ChatbotAnalytics()

# Create prompt template with LinkedIn integration
prompt_template = """Given the following context about Noah's professional background and a question,
provide a concise, professional response highlighting relevant skills, achievements, and experiences.

Guidelines:
- Be specific and pull concrete details from the context when available
- Maintain a professional, interview-appropriate tone
- If information is not in the context, briefly say you don't know rather than inventing details
- When the question asks about roles, work history, or how to connect, include Noah's LinkedIn URL: {linkedin_url}

CONTEXT: {context}

QUESTION: {question}

RESPONSE:"""

PROMPT = PromptTemplate(
    template=prompt_template, 
    input_variables=["context", "question"],
    partial_variables={"linkedin_url": config.LINKEDIN_URL or ""}
)
chain = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=retriever, 
    input_key="query", 
    return_source_documents=True, 
    chain_type_kwargs={"prompt": PROMPT}
)

# Test questions
sample_questions = [
    "Walk me through Noah's career so far",
    "How can I connect with Noah professionally?", 
    "What technical skills does Noah have?",
    "Why did Noah transition from sales to AI/software?"
]

# CHANGE THIS QUESTION TO TEST DIFFERENT ONES:
question = "Walk me through Noah's career so far"

print(f"🤔 Question: {question}")
print("=" * 50)

# Get answer with timing
start_time = time.time()
result = chain.invoke({"query": question})
response_time_ms = (time.time() - start_time) * 1000

answer = result['result']
source_docs = result['source_documents']

# Analyze response
career_keywords = ["career", "background", "experience", "work", "job", "role", "linkedin", "connect", "history"]
is_career_related = any(keyword in question.lower() for keyword in career_keywords)
linkedin_included = config.LINKEDIN_URL in answer if config.LINKEDIN_URL else False

# Log analytics
analytics.log_interaction(
    question=question,
    answer=answer,
    source_count=len(source_docs),
    response_time_ms=response_time_ms,
    linkedin_included=linkedin_included,
    is_career_related=is_career_related,
    session_id="single_question_test"
)

# Display results
print(f"🎯 Answer:\n{answer}")
print(f"\n📚 Sources used: {len(source_docs)}")
print(f"⏱️  Response time: {response_time_ms:.1f}ms")

if is_career_related:
    if linkedin_included:
        print("✅ LinkedIn URL automatically included!")
    else:
        print(f"ℹ️  LinkedIn URL available: {config.LINKEDIN_URL}")

# Show analytics summary
print("\n📊 Analytics logged!")
stats = analytics.get_analytics_summary()
print(f"Total interactions logged: {stats.get('total_interactions', 0)}")

print("\n" + "=" * 50)
print("💡 Try these sample questions:")
for i, q in enumerate(sample_questions, 1):
    print(f"{i}. {q}")