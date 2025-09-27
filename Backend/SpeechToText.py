import speech_recognition as sr
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "es-US")
WakeWord = env_vars.get("WAKE_WORD", "hey jarvis")

recognizer = sr.Recognizer()
mic = sr.Microphone()

def listen() -> str:
    try:
        with mic as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio, language=InputLanguage).lower()
        print(f"You said: {text}")
        return text
    except Exception:
        return ""
    
def listen_for_wakeword() -> str:
    """Listen until wakeword is detected"""
    while True:
        text = listen()
        if WakeWord in text:
            return "Wakeword detected"