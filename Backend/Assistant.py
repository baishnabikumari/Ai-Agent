from Backend.Chatbot import get_response

def process_command(user_input: str) -> str:
    if not user_input:
        return "I didn’t catch that."
    return get_response(user_input)
