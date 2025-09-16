from dotenv import load_dotenv
import os
from openai import OpenAI

def test_api_key():
    try:
        # Load the API key from .env
        load_dotenv()
        api_key = os.environ["OPENAI_API_KEY"]
        
        print(f"API Key format: {api_key[:7]}...{api_key[-4:]}")
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        print("Client initialized, attempting API call...")
        
        # Try a simple API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Try with a different model
            messages=[{"role": "user", "content": "Hi, this is a test message."}],
            max_tokens=5
        )
        
        print("✅ API key is valid and working!")
        return True
        
    except Exception as e:
        print("❌ Error testing API key:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        return False

if __name__ == "__main__":
    test_api_key()
