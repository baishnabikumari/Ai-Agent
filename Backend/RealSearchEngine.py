import datetime
import os
from googlesearch import search
from groq import Groq
from json import load, dump
from dotenv import load_dotenv

# Load .env from Backend folder
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

Username = os.getenv("Username")
Assistantname = os.getenv("Assistantname")
GroqAPIKey = os.getenv("GROQ_API_KEY")

if not GroqAPIKey:
    raise ValueError("GROQ_API_KEY not found in Backend/.env")

client = Groq(api_key=GroqAPIKey)

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Initialize chatbot memory
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

# Ensure ChatLog.json exists
chatlog_path = os.path.join(os.path.dirname(__file__), "Data", "ChatLog.json")
os.makedirs(os.path.dirname(chatlog_path), exist_ok=True)
if not os.path.exists(chatlog_path):
    with open(chatlog_path, "w") as f:
        dump([], f)

def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    answer = ""
    for i in results:
        answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    answer += "[end]"
    return answer

def AnswerModifier(answer):
    lines = answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def Information():
    current_date_time = datetime.datetime.now()
    data = (
        f"Use This Real-time Information if needed:\n"
        f"Day: {current_date_time.strftime('%A')}\n"
        f"Date: {current_date_time.strftime('%d')}\n"
        f"Month: {current_date_time.strftime('%B')}\n"
        f"Year: {current_date_time.strftime('%Y')}\n"
        f"Time: {current_date_time.strftime('%H')} hours, "
        f"{current_date_time.strftime('%M')} minutes, "
        f"{current_date_time.strftime('%S')} seconds.\n"
    )
    return data

def RealtimeSearchEngine(prompt):
    global SystemChatBot

    with open(chatlog_path, "r") as f:
        messages = load(f)

    messages.append({"role": "user", "content": prompt})
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
    )

    answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content

    answer = answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": answer})

    with open(chatlog_path, "w") as f:
        dump(messages, f, indent=4)

    SystemChatBot.pop()
    return AnswerModifier(answer)

if __name__ == "__main__":
    while True:
        prompt = input("Enter your Query: ")
        print(RealtimeSearchEngine(prompt))
