# Backend/Assistant.py
import cohere
from Backend.config import get_api_key, get_model

# Initialize Cohere client
api_key = get_api_key()
co = cohere.Client(api_key) if api_key else None
model = get_model()

def process_command(user_message: str) -> str:
    """
    Send user message to Cohere Chat API and return response.
    """
    if not co:
        return "[Error] Missing API key. Please set COHERE_API_KEY in .env"

    try:
        response = co.chat(
            model=model,
            message=user_message
        )
        return response.text.strip()
    except Exception as e:
        return f"[Error] {str(e)}"
