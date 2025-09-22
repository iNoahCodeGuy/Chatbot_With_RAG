import streamlit as st

# Minimal test version to check if basic Streamlit works
st.set_page_config(
    page_title="Noah's Portfolio Q&A - Test",
    page_icon="💼",
    layout="wide"
)

st.title("Noah's Portfolio Q&A Test 💼")

# Test if we can access secrets
try:
    api_key = st.secrets.get("OPENAI_API_KEY")
    if api_key:
        st.success("✅ API key found in secrets!")
        st.write(f"Key starts with: {api_key[:10]}...")
    else:
        st.error("❌ API key not found in secrets")
except Exception as e:
    st.error(f"❌ Error accessing secrets: {e}")

st.write("If you can see this, basic Streamlit is working!")

# Add a simple test button
if st.button("Test Button"):
    st.balloons()
    st.success("Button works!")






