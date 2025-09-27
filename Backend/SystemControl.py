import os
import datetime
import webbrowser
import psutil

def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def get_date():
    return datetime.datetime.now().strftime('%A, %d %B %Y')

def open_browser(url="https://www.google.com"):
    webbrowser.open(url)
    return "Opening Browser..."

def open_app(app_name: str):
    if "chrome" in app.name.lower():
        return "Opening Google Chrome..."
    elif "vscode" in app_name.lower():
        os.system("open -a 'Visual Studio Code'")
        return "Opening VS Code..."
    else:
        return "App not Configured."

def system_status():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    battery = psutil.sensors_battery().percent if psutil.sensors_battery() else "N/A"
    return f"CPU: {cpu}% | Memory: {memory}% | Battery: {battery}%"


