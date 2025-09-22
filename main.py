import streamlit as st
from langchain_helper import get_qa_chain, create_vector_db

st.title("Noah's Portfolio Q&A 💼")
btn = st.button("Create Knowledge Base")
if btn:
    create_vector_db()

question = st.text_input("Ask about Noah's professional background: ")

if question:
    chain = get_qa_chain()
    response = chain(question)

    st.header("Answer")
    st.write(response["result"])






