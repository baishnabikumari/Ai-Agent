# Backend/Chatbot.py

import os
from dotenv import load_dotenv
import cohere

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("Missing COHERE_API_KEY in .env")

co = cohere.Client(COHERE_API_KEY)

def get_response(user_input: str) -> str:
    try:
        response = co.chat(
            model="command-a-03-2025",
            message=user_input
        )
        return response.text.strip()
    except Exception as e:
        return f"Jarvis Error: {e}"
