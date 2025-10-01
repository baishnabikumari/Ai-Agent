# Backend/Chatbot.py
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_response(command, mode="chat"):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4 if you have access
            messages=[
                {"role": "system", "content": "You are Jarvis AI, a helpful assistant."},
                {"role": "user", "content": command}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"
