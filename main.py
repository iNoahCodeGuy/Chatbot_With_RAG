import streamlit as st
import os
from config import Config

# Configure the page
st.set_page_config(
    page_title="Noah's Portfolio Q&A",
    page_icon="💼",
    layout="wide"
)

st.title("Noah's Portfolio Q&A 💼")

# Check if API key is configured
config = Config()
if not config.OPENAI_API_KEY:
    st.error("⚠️ OpenAI API key not configured. Please check your Streamlit secrets.")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("Knowledge Base")
    if st.button("🔄 Create/Update Knowledge Base"):
        with st.spinner("Creating knowledge base..."):
            try:
                from langchain_helper import create_vector_db
                create_vector_db()
                st.success("✅ Knowledge base created successfully!")
            except Exception as e:
                st.error(f"❌ Error creating knowledge base: {str(e)}")

    st.markdown("---")
    st.subheader("Sample Questions:")
    st.markdown("""
    - What is Noah's professional background?
    - What programming languages does Noah know?
    - Tell me about Noah's work experience
    - What projects has Noah worked on?
    """)

# Main interface
question = st.text_input("Ask about Noah's professional background:", placeholder="Type your question here...")

if question:
    with st.spinner("Thinking..."):
        try:
            from langchain_helper import get_qa_chain
            chain = get_qa_chain()
            response = chain(question)
            
            st.header("Answer")
            st.write(response["result"])
            
            # Show sources if available
            if "source_documents" in response and response["source_documents"]:
                with st.expander("📚 Sources"):
                    for i, doc in enumerate(response["source_documents"]):
                        st.text(f"Source {i+1}: {doc.page_content[:200]}...")
                        
        except Exception as e:
            st.error(f"❌ Error processing question: {str(e)}")
            st.info("Please make sure the knowledge base is created and your API key is configured.")






