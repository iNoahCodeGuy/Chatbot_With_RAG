# Import required LangChain components
from langchain_community.vectorstores import FAISS  # Vector database for storing and searching embeddings
from langchain_openai import ChatOpenAI  # OpenAI's chat model interface
from langchain_community.document_loaders.csv_loader import CSVLoader  # For loading CSV data (you'll change this for your portfolio)
from langchain_openai import OpenAIEmbeddings  # For creating text embeddings
from langchain.prompts import PromptTemplate  # For creating custom prompt templates
from langchain.chains import RetrievalQA  # For building Q&A chain
from config import config  # Import centralized configuration

# Validate configuration on import
config.validate()

# Initialize the language model using configuration
llm = ChatOpenAI(
    model=config.OPENAI_MODEL,
    temperature=config.OPENAI_TEMPERATURE,
    openai_api_key=config.OPENAI_API_KEY
)
# # Initialize embeddings model using configuration
openai_embeddings = OpenAIEmbeddings(
    model=config.OPENAI_EMBEDDING_MODEL,
    openai_api_key=config.OPENAI_API_KEY
)

# Path where the vector database will be saved
vectordb_file_path = config.VECTOR_DB_PATH

def create_vector_db():
    """
    Creates a vector database from your professional experience data.
    For your portfolio, you'll want to:
    1. Create a CSV with columns like:
       - experience: Your work history, projects, skills
       - context: Additional details, technologies used
       - achievements: Specific accomplishments
    2. Modify the CSVLoader parameters to match your CSV structure
    """
    # Load your professional experience data using configuration
    loader = CSVLoader(
        file_path=config.CSV_FILE_PATH,
        source_column=config.SOURCE_COLUMN
    )
    data = loader.load()

    # Convert your experience data into vectors for semantic search
    vectordb = FAISS.from_documents(
        documents=data,
        embedding=openai_embeddings  # Uses OpenAI embeddings to create embeddings
    )

    # Save the vector database locally for quick access
    vectordb.save_local(vectordb_file_path)


def get_qa_chain():
    """
    Creates a question-answering chain that:
    1. Loads your pre-created vector database
    2. Sets up a retriever to find relevant experience/skills
    3. Uses a custom prompt to format responses professionally
    4. Returns a chain that can answer questions about your experience
    """
    # Load the vector database from the local folder
    vectordb = FAISS.load_local(vectordb_file_path, openai_embeddings)

    # Create a retriever for querying the vector database using configuration
    retriever = vectordb.as_retriever(score_threshold=config.RETRIEVER_SCORE_THRESHOLD)

    # Define how the AI should respond to questions
    # - Encourages professional, detailed responses
    # - Maintains accuracy by sticking to provided context
    prompt_template = """Given the following context about the candidate's professional experience and a question, 
    provide a detailed, professional response. Focus on highlighting relevant skills, achievements, and experiences.

    Guidelines:
    - Be specific and provide concrete examples from the context
    - Highlight relevant technical skills and achievements
    - Maintain a professional, interview-appropriate tone
    - If information is not in the context, politely acknowledge the limitation

    CONTEXT: {context}

    QUESTION: {question}

    PROFESSIONAL RESPONSE:"""

    # Create the prompt template with our variables
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    # Build the QA chain
    # - Uses the language model for generating responses
    # - Retrieves relevant context from your experience
    # - Returns source documents for transparency
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        input_key="query",
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )

    return chain

if __name__ == "__main__":
    create_vector_db()
    chain = get_qa_chain()
    print(chain("Do you have javascript course?"))