# Backend/config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_api_key() -> str:
    """
    Get Cohere API key from .env
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        print("[Warning] COHERE_API_KEY not found in .env")
    return api_key or ""

def get_model() -> str:
    """
    Get Cohere model from .env (default = command-r-v1.0)
    """
    return os.getenv("COHERE_MODEL", "command-r-v1.0")
