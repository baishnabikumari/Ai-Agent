import os
from dotenv import load_dotenv
import openai
from groq import Groq

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

openai.api_key = OPENAI_API_KEY
groq_client = Groq(api_key=GROQ_API_KEY)

def query_openai(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error (OpenAI): {str(e)}"
    
def query_groq(prompt: str) -> str:
    try:
        response = groq_client.chat.completion.create(
            model='llama3-8b-8192',
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error (Groq): {str(e)}"

