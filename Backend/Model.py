# Backend/model.py
import os
import cohere
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Initialize client
co = cohere.Client(api_key=COHERE_API_KEY)

def query_ai(prompt: str) -> str:
    """
    Send a prompt to Cohere and return the AI's response.
    """
    try:
        response = co.chat(
            model="command-r-plus",  # Cohere's latest best chat model
            message=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"[Error: {str(e)}]"
