import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id) # Hope This is female Voice

def speak(text: str):
    print(f" Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()
    