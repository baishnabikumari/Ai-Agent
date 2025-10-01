from Backend.Chatbot import get_response

def process_command(command: str) -> str:
    # Add any special command handling (time, open, search) here if you want
    return get_response(command)
