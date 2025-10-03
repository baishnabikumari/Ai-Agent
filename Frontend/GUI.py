# Frontend/gui.py
import tkinter as tk
from tkinter import Scrollbar, Canvas
from PIL import Image, ImageTk
import os
import sys
import threading
from datetime import datetime
from Backend.Assistant import process_command

# helper to find bundled resources (works with PyInstaller onefile)
def resource_path(rel_path):
    try:
        base = sys._MEIPASS  # created by PyInstaller
    except Exception:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base, rel_path)

ASSETS_PATH = resource_path("assets")

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis AI")
        self.root.geometry("400x700")
        self.root.resizable(False, False)
        self.images = {}

        self._create_header()
        self._create_chat_area()
        self._create_input_area()

    def _create_header(self):
        header_frame = tk.Frame(self.root, height=100, bg="white")
        header_frame.pack(fill="x")

        # Jarvis logo (top) - optional
        try:
            jarvis_img = Image.open(os.path.join(ASSETS_PATH, "jarvis.png")).resize((50, 50))
            self.images["header_jarvis"] = ImageTk.PhotoImage(jarvis_img)
            tk.Label(header_frame, image=self.images["header_jarvis"], bg="white").pack(pady=5)
        except Exception:
            tk.Label(header_frame, text="", bg="white").pack(pady=5)

        tk.Label(header_frame, text="Jarvis AI", font=("Helvetica", 16, "bold"), bg="white").pack()
        tk.Label(header_frame, text="Online", font=("Helvetica", 10), fg="gray", bg="white").pack()

    def _create_chat_area(self):
        container = tk.Frame(self.root, bg="white")
        container.pack(fill="both", expand=True)

        self.canvas = Canvas(container, bg="white", highlightthickness=0)
        self.scrollbar = Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.chat_frame = tk.Frame(self.canvas, bg="white")

        self.chat_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _create_input_area(self):
        input_frame = tk.Frame(self.root, bg="white", height=60)
        input_frame.pack(fill="x", side="bottom")

        self.entry = tk.Entry(
            input_frame,
            font=("Helvetica", 14),
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.entry.pack(fill="x", padx=10, pady=10, side="left", expand=True)
        self.entry.bind("<Return>", self.send_message)

        # send icon
        try:
            send_img = Image.open(os.path.join(ASSETS_PATH, "send.png")).resize((30, 30))
            self.images["send_icon"] = ImageTk.PhotoImage(send_img)
            send_btn = tk.Button(input_frame, image=self.images["send_icon"], bg="white", relief="flat", command=self.send_message)
        except Exception:
            send_btn = tk.Button(input_frame, text="Send", bg="white", relief="flat", command=self.send_message)
        send_btn.pack(side="right", padx=5)

    def _add_message(self, message, sender="user"):
        outer_frame = tk.Frame(self.chat_frame, bg="white")

        if sender == "user":
            # User bubble
            try:
                user_img = Image.open(os.path.join(ASSETS_PATH, "user.png")).resize((35, 35))
                self.images["user_icon"] = ImageTk.PhotoImage(user_img)
                user_icon_label = tk.Label(outer_frame, image=self.images["user_icon"], bg="white")
            except Exception:
                user_icon_label = None

            frame = tk.Frame(outer_frame, bg="white")
            bubble = tk.Frame(frame, bg="#8B0000", padx=10, pady=5)
            text_label = tk.Label(bubble, text=message, font=("Helvetica", 12),
                                  bg="#8B0000", fg="white", wraplength=220, justify="left")
            text_label.pack(anchor="e")
            time_label = tk.Label(bubble, text=self._get_timestamp(), font=("Helvetica", 8),
                                  fg="lightgray", bg="#8B0000")
            time_label.pack(anchor="e")
            bubble.pack(side="right")

            if user_icon_label:
                user_icon_label.pack(side="right", padx=5, anchor="s")
            frame.pack(side="right")

        elif sender == "bot":
            # Bot bubble
            try:
                bot_img = Image.open(os.path.join(ASSETS_PATH, "jarvis.png")).resize((35, 35))
                self.images["bot_icon"] = ImageTk.PhotoImage(bot_img)
                bot_icon_label = tk.Label(outer_frame, image=self.images["bot_icon"], bg="white")
            except Exception:
                bot_icon_label = None

            frame = tk.Frame(outer_frame, bg="white")
            if bot_icon_label:
                bot_icon_label.pack(side="left", padx=5, anchor="s")

            bubble = tk.Frame(frame, bg="black", padx=10, pady=5)
            text_label = tk.Label(bubble, text=message, font=("Helvetica", 12),
                                  bg="black", fg="white", wraplength=220, justify="left")
            text_label.pack(anchor="w")
            time_label = tk.Label(bubble, text=self._get_timestamp(), font=("Helvetica", 8),
                                  fg="lightgray", bg="black")
            time_label.pack(anchor="e")
            bubble.pack(side="left")
            frame.pack(side="left")

        elif sender == "error":
            # Error bubble (red)
            frame = tk.Frame(outer_frame, bg="white")
            bubble = tk.Frame(frame, bg="#B22222", padx=10, pady=5)
            text_label = tk.Label(bubble, text=message, font=("Helvetica", 12),
                                  bg="#B22222", fg="white", wraplength=220, justify="left")
            text_label.pack(anchor="w")
            time_label = tk.Label(bubble, text=self._get_timestamp(), font=("Helvetica", 8),
                                  fg="lightgray", bg="#B22222")
            time_label.pack(anchor="e")
            bubble.pack(side="left")
            frame.pack(side="left")

        outer_frame.pack(anchor="w" if sender in ("bot", "error") else "e", pady=5, padx=10)
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def send_message(self, event=None):
        user_message = self.entry.get().strip()
        if not user_message:
            return
        self._add_message(user_message, "user")
        self.entry.delete(0, "end")

        # run AI call in background thread so UI doesn't freeze
        def worker():
            ai_response = process_command(user_message)

            def show_reply():
                if ai_response.startswith("[Error]"):
                    self._add_message(ai_response, "error")
                else:
                    self._add_message(ai_response, "bot")

            self.root.after(0, show_reply)

        threading.Thread(target=worker, daemon=True).start()

    def _get_timestamp(self):
        return datetime.now().strftime("%H:%M")


def run_gui():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
