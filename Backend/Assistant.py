from Backend.Chatbot import get_response
from Backend.SystemControl import get_time, get_date, open_browser, open_app, system_status
from Backend.Tools import web_search

def process_command(command: str, mode="auto") -> str:
    command = command.lower()

    if "time" in command:
        return f"The current TIME is {get_time()}."
    elif "date" in command:
        return f"Today's date is {get_date()}."
    elif "open browser" in command:
        return open_browser()
    elif "open" in command:
        return open.app(command.replace("open", "").strip())
    elif "status" in command:
        return system_status()
    elif "search" in command:
        return web_search(command.replace("search", "").strip())
    
    return get_response(command)
    