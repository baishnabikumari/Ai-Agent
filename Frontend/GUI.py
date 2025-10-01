import tkinter as tk
from tkinter import ttk
from datetime import datetime
from Backend.Assistant import process_command


# ===================== MAIN APP =====================
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis AI")
        self.root.geometry("1100x700")
        self.root.configure(bg="#1e1e1e")  # Dark theme background
        self.root.resizable(False, False)

        # ---------- LAYOUT ----------
        self.create_sidebar()
        self.create_header()
        self.create_chat_area()
        self.create_input_area()

        # Track conversations
        self.current_conversation = []
        self.conversations = []

    # ===================== SIDEBAR =====================
    def create_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg="#0f3d3e", width=200)
        self.sidebar.pack(side="left", fill="y")

        sidebar_title = tk.Label(
            self.sidebar, text="Conversations",
            font=("Arial", 14, "bold"), fg="white", bg="#0f3d3e"
        )
        sidebar_title.pack(pady=10)

        self.conversation_list = tk.Listbox(
            self.sidebar, bg="#0f3d3e", fg="white",
            font=("Arial", 11), bd=0, highlightthickness=0,
            selectbackground="#135d5f", activestyle="none"
        )
        self.conversation_list.pack(fill="both", expand=True, padx=5, pady=5)

    # ===================== HEADER =====================
    def create_header(self):
        self.header = tk.Frame(self.root, bg="#135d5f", height=50)
        self.header.pack(side="top", fill="x")

        self.title_label = tk.Label(
            self.header, text="J.A.R.V.I.S Online",
            font=("Arial", 16, "bold"), fg="white", bg="#135d5f"
        )
        self.title_label.pack(side="left", padx=20)

    # ===================== CHAT AREA =====================
    def create_chat_area(self):
        self.chat_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.chat_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Scrollable canvas
        self.canvas = tk.Canvas(self.chat_frame, bg="#1e1e1e", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1e1e1e")

        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    # ===================== INPUT AREA =====================
    def create_input_area(self):
        self.input_frame = tk.Frame(self.root, bg="#1e1e1e", height=50)
        self.input_frame.pack(side="bottom", fill="x", pady=5)

        self.entry = tk.Entry(
            self.input_frame, bg="#2c2c2c", fg="white",
            font=("Arial", 13), insertbackground="white", relief="flat"
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=5, ipady=8)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            self.input_frame, text="Send", command=self.send_message,
            bg="#0f3d3e", fg="white", font=("Arial", 12, "bold"),
            relief="flat", activebackground="#135d5f", activeforeground="white",
            width=10
        )
        self.send_button.pack(side="right", padx=(5, 10), pady=5)

    # ===================== MESSAGE HANDLING =====================
    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return

        # Add user message
        self.add_message("You", user_input, "user")
        self.entry.delete(0, tk.END)

        # Process AI response
        response = process_command(user_input)
        self.add_message("Jarvis", response, "bot")

        # Save to conversation
        self.current_conversation.append((user_input, response))
        self.update_conversation_list()

    def add_message(self, sender, text, sender_type):
        msg_frame = tk.Frame(self.scrollable_frame, bg="#1e1e1e")
        msg_frame.pack(fill="x", pady=5, padx=10)

        if sender_type == "user":
            bubble = tk.Label(
                msg_frame, text=text, wraplength=700,
                bg="#135d5f", fg="white", font=("Arial", 12),
                padx=10, pady=6, anchor="e", justify="left"
            )
            bubble.pack(anchor="e", padx=10)

        else:  # bot
            bubble = tk.Label(
                msg_frame, text=text, wraplength=700,
                bg="#2c2c2c", fg="white", font=("Arial", 12),
                padx=10, pady=6, anchor="w", justify="left"
            )
            bubble.pack(anchor="w", padx=10)

        # Auto-scroll to bottom
        self.root.after(100, lambda: self.canvas.yview_moveto(1.0))

    def update_conversation_list(self):
        """Update sidebar with last message preview + timestamp."""
        if self.current_conversation:
            last_user, _ = self.current_conversation[-1]
            preview = (last_user[:20] + "...") if len(last_user) > 20 else last_user
            timestamp = datetime.now().strftime("%I:%M %p")
            self.conversation_list.insert(tk.END, f"{preview}   {timestamp}")


# ===================== RUN APP =====================
def run_gui():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
