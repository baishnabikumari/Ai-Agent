import tkinter as tk
from tkinter import Scrollbar, Canvas
from PIL import Image, ImageTk
import os
from datetime import datetime
from Backend.Assistant import process_command

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "..", "assets")

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

        # Jarvis logo (top)
        jarvis_img = Image.open(os.path.join(ASSETS_PATH, "jarvis.png")).resize((50, 50))
        self.images["header_jarvis"] = ImageTk.PhotoImage(jarvis_img)

        tk.Label(header_frame, image=self.images["header_jarvis"], bg="white").pack(pady=5)
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
            bg="#1e1e1e",              # dark background
            fg="white",                # white text
            insertbackground="white",  # white cursor
            relief="flat"
        )
        self.entry.pack(fill="x", padx=10, pady=10, side="left", expand=True)
        self.entry.bind("<Return>", self.send_message)

        send_img = Image.open(os.path.join(ASSETS_PATH, "send.png")).resize((30, 30))
        self.images["send_icon"] = ImageTk.PhotoImage(send_img)

        send_btn = tk.Button(
            input_frame,
            image=self.images["send_icon"],
            bg="white",
            relief="flat",
            command=self.send_message
        )
        send_btn.pack(side="right", padx=5)

    def _add_message(self, message, sender="user"):
        outer_frame = tk.Frame(self.chat_frame, bg="white")

        if sender == "user":
            user_img = Image.open(os.path.join(ASSETS_PATH, "user.png")).resize((35, 35))
            self.images["user_icon"] = ImageTk.PhotoImage(user_img)

            frame = tk.Frame(outer_frame, bg="white")

            bubble = tk.Frame(frame, bg="#8B0000", padx=10, pady=5)
            text_label = tk.Label(
                bubble, text=message,
                font=("Helvetica", 12),
                bg="#8B0000", fg="white",
                wraplength=220, justify="left"
            )
            text_label.pack(anchor="e")

            time_label = tk.Label(
                bubble, text=self._get_timestamp(),
                font=("Helvetica", 8),
                fg="lightgray", bg="#8B0000"
            )
            time_label.pack(anchor="e")

            bubble.pack(side="right")
            tk.Label(frame, image=self.images["user_icon"], bg="white").pack(side="right", padx=5, anchor="s")
            frame.pack(side="right")

        else:
            bot_img = Image.open(os.path.join(ASSETS_PATH, "jarvis.png")).resize((35, 35))
            self.images["bot_icon"] = ImageTk.PhotoImage(bot_img)

            frame = tk.Frame(outer_frame, bg="white")

            tk.Label(frame, image=self.images["bot_icon"], bg="white").pack(side="left", padx=5, anchor="s")

            bubble = tk.Frame(frame, bg="black", padx=10, pady=5)
            text_label = tk.Label(
                bubble, text=message,
                font=("Helvetica", 12),
                bg="black", fg="white",
                wraplength=220, justify="left"
            )
            text_label.pack(anchor="w")

            time_label = tk.Label(
                bubble, text=self._get_timestamp(),
                font=("Helvetica", 8),
                fg="lightgray", bg="black"
            )
            time_label.pack(anchor="e")

            bubble.pack(side="left")
            frame.pack(side="left")

        outer_frame.pack(anchor="w" if sender == "bot" else "e", pady=5, padx=10)
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def send_message(self, event=None):
        user_message = self.entry.get().strip()
        if not user_message:
            return
        self._add_message(user_message, "user")
        self.entry.delete(0, "end")

        ai_response = process_command(user_message)
        self._add_message(ai_response, "bot")

    def _get_timestamp(self):
        return datetime.now().strftime("%H:%M")


def run_gui():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
