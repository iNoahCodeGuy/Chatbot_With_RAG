import streamlit as st
from langchain_helper import get_qa_chain, create_vector_db
import os

# Page configuration
st.set_page_config(
    page_title="Noah's Portfolio Q&A",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and header
st.title("Noah's Portfolio Q&A 💼")
st.markdown("Ask me anything about Noah's professional background, skills, and experience!")

# Sidebar for setup
with st.sidebar:
    st.header("Setup")
    if st.button("🚀 Initialize Knowledge Base", type="primary"):
        with st.spinner("Creating knowledge base... This may take a moment."):
            try:
                create_vector_db()
                st.success("✅ Knowledge base created successfully!")
            except Exception as e:
                st.error(f"❌ Error creating knowledge base: {str(e)}")
    
    st.markdown("---")
    st.markdown("**Sample Questions:**")
    st.markdown("• What is Noah's educational background?")
    st.markdown("• Tell me about Noah's sales experience")
    st.markdown("• What skills does Noah have?")
    st.markdown("• What certifications does Noah have?")

# Main Q&A interface
question = st.text_input(
    "Ask about Noah's professional background:",
    placeholder="e.g., What is Noah's educational background?"
)

if question:
    with st.spinner("Thinking..."):
        try:
            chain = get_qa_chain()
            response = chain(question)
            
            st.header("💡 Answer")
            st.write(response["result"])
            
            # Show sources if available
            if "source_documents" in response and response["source_documents"]:
                with st.expander("📚 View Sources"):
                    for i, doc in enumerate(response["source_documents"], 1):
                        st.write(f"**Source {i}:**")
                        st.write(doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content)
                        st.write("---")
                        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("💡 Make sure to initialize the knowledge base first using the button in the sidebar.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and LangChain")






