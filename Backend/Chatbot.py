import os
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

# --- 1. Load .env from correct location ---
backend_env = os.path.join(os.path.dirname(__file__), ".env")
root_env = os.path.join(os.path.dirname(__file__), "..", ".env")

if os.path.exists(backend_env):
    env_vars = dotenv_values(backend_env)
elif os.path.exists(root_env):
    env_vars = dotenv_values(root_env)
else:
    env_vars = {}

# --- 2. Load variables ---
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

# --- 3. Debugging ---
print("Loaded API Key:", GroqAPIKey)

# --- 4. Error if key is missing ---
if not GroqAPIKey:
    raise ValueError("GROQ_API_KEY not found. Please add it to .env or set it as an environment variable.")

# --- 5. Initialize Groq client ---
client = Groq(api_key=GroqAPIKey)

# --- 6. Prepare system message ---
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [
    {"role": "system", "content": System}
]

# --- 7. Ensure chatLog.json exists ---
chat_log_path = os.path.join(os.path.dirname(__file__), "Data", "chatLog.json")
os.makedirs(os.path.dirname(chat_log_path), exist_ok=True)

if not os.path.exists(chat_log_path):
    with open(chat_log_path, "w") as f:
        dump([], f)

# --- 8. Real-time info helper ---
def RealtimeInformation():
    now = datetime.datetime.now()
    return (
        f"Please use this real-time information if needed,\n"
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d')}\n"
        f"Month: {now.strftime('%B')}\n"
        f"Year: {now.strftime('%Y')}\n"
        f"Time: {now.strftime('%H')} hours :{now.strftime('%M')} minutes :{now.strftime('%S')} seconds.\n"
    )

# --- 9. Chatbot function ---
def ChatBot(Query):
    """Send user query to the chatbot and return AI's response."""
    try:
        with open(chat_log_path, "r") as f:
            messages = load(f)

        messages.append({"role": "user", "content": Query})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=SystemChatBot + [{"role": "user", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})

        with open(chat_log_path, "w") as f:
            dump(messages, f, indent=4)

        return Answer

    except Exception as e:
        print(f"Error: {e}")
        with open(chat_log_path, "w") as f:
            dump([], f, indent=4)
        return "Sorry, something went wrong. Please try again."

# --- 10. Run chatbot loop ---
if __name__ == "__main__":
    while True:
        user_input = input("Enter your Question: ")
        print(ChatBot(user_input))
