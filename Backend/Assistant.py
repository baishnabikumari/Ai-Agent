import os
import cohere

# Try both env variable names
api_key = os.getenv("COHERE_API_KEY") or os.getenv("CO_API_KEY")

if not api_key:
    raise ValueError("❌ No Cohere API key found. Please set COHERE_API_KEY or CO_API_KEY.")

# Initialize Cohere client
cohere_client = cohere.Client(api_key)

def process_command(user_input: str) -> str:
    """
    Process the user input using Cohere API and return the AI response.
    """
    try:
        response = cohere_client.chat(
            model="command-r",   # ✅ Updated model
            message=user_input
        )
        return response.text.strip()

    except Exception as e:
        print(f"[Cohere Error] {e}")
        return "⚠️ Sorry, I had trouble connecting to AI. Please try again later."
