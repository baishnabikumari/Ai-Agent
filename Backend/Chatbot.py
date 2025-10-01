# Backend/Chatbot.py

import os
from dotenv import load_dotenv
import cohere

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise ValueError("❌ COHERE_API_KEY not found in environment")

co = cohere.Client(COHERE_API_KEY)

def get_response(prompt: str) -> str:
    try:
        # Correct Cohere chat usage
        response = co.chat(
            model="command-a-03-2025",  # ✅ valid Cohere model
            message=prompt              # ✅ use "message", not "messages"
        )
        return response.text.strip()
    except Exception as e:
        return f"Jarvis Error: {e}"
