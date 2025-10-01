# Frontend/gui.py
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
from Backend.Assistant import process_command

# Assets path
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(HERE, "assets")

def load_image(name, size=None):
    path = os.path.join(ASSETS_DIR, name)
    try:
        img = Image.open(path)
        if size:
            img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"[Assets] Error loading {path}: {e}")
        return None


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis AI")
        self.WIDTH, self.HEIGHT = 400, 740
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.resizable(False, False)

        # Images
        self.bg_img = load_image("bg.jpg", size=(self.WIDTH, self.HEIGHT))
        self.bot_avatar = load_image("jarvis.png", size=(36, 36))
        self.user_avatar = load_image("user.png", size=(36, 36))
        self.send_icon = load_image("send.png", size=(28, 28))

        # Background
        if self.bg_img:
            self.bg_label = tk.Label(self.root, image=self.bg_img)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.root.configure(bg="white")

        self._create_header()
        self._create_chat_area()
        self._create_input_area()

    def _create_header(self):
        h = tk.Frame(self.root, bg="white", bd=0)
        h.place(x=0, y=6, width=self.WIDTH, height=110)

        if self.bot_avatar:
            logo = tk.Label(h, image=self.bot_avatar, bg="white")
            logo.place(relx=0.5, x=-18, y=10)

        title = tk.Label(h, text="Jarvis AI", bg="white", fg="#222222",
                         font=("Arial", 14, "bold"))
        title.place(relx=0.5, y=72, anchor="center")

        subtitle = tk.Label(h, text="Online", bg="white", fg="#666666",
                            font=("Arial", 9))
        subtitle.place(relx=0.5, y=94, anchor="center")

    def _create_chat_area(self):
        top = 120
        bottom = 80
        area_h = self.HEIGHT - top - bottom

        container = tk.Frame(self.root, bg="white", bd=0)
        container.place(x=0, y=top, width=self.WIDTH, height=area_h)

        self.canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable = tk.Frame(self.canvas, bg="white")

        self.scrollable.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _create_input_area(self):
        input_h = 68
        frame = tk.Frame(self.root, bg="white")
        frame.place(x=10, y=self.HEIGHT - input_h, width=self.WIDTH - 20, height=input_h - 6)

        # Entry
        self.entry = tk.Entry(frame, font=("Helvetica", 12), fg="#999999", bd=0)
        self.entry.insert(0, "How may i help you ?")
        self.entry.bind("<FocusIn>", self._clear_placeholder)
        self.entry.bind("<FocusOut>", self._set_placeholder)
        self.entry.bind("<Return>", lambda e: self.send_message())
        self.entry.place(x=18, y=12, width=self.WIDTH - 110, height=40)

        # Send button
        if self.send_icon:
            btn = tk.Button(frame, image=self.send_icon, bd=0, bg="white",
                            activebackground="white", cursor="hand2",
                            command=self.send_message)
        else:
            btn = tk.Button(frame, text="Send", bd=0, bg="#10A37F", fg="white",
                            command=self.send_message)
        btn.place(x=self.WIDTH - 82, y=8, width=60, height=48)

    def _clear_placeholder(self, event=None):
        if self.entry.get().strip() == "How may i help you ?":
            self.entry.delete(0, tk.END)
            self.entry.config(fg="#222222")

    def _set_placeholder(self, event=None):
        if not self.entry.get().strip():
            self.entry.insert(0, "How may i help you ?")
            self.entry.config(fg="#999999")

    def _add_bot_message(self, text):
        row = tk.Frame(self.scrollable, bg="white", pady=6)
        row.pack(fill="x", anchor="w", padx=12)

        if self.bot_avatar:
            av = tk.Label(row, image=self.bot_avatar, bg="white")
            av.pack(side="left", padx=(4, 6))

        bubble = tk.Label(row, text=text, wraplength=240, justify="left",
                          bg="#ffffff", fg="#222222", padx=12, pady=8,
                          font=("Arial", 11), bd=0, relief="flat")
        bubble.pack(side="left")

        self._autoscroll()

    def _add_user_message(self, text):
        row = tk.Frame(self.scrollable, bg="white", pady=6)
        row.pack(fill="x", anchor="e", padx=12)

        bubble = tk.Label(row, text=text, wraplength=240, justify="left",
                          bg="#f7f7f7", fg="#222222", padx=12, pady=8,
                          font=("Arial", 11), bd=0, relief="flat")
        bubble.pack(side="right", padx=(6, 4))

        if self.user_avatar:
            av = tk.Label(row, image=self.user_avatar, bg="white")
            av.pack(side="right", padx=(6, 4))

        self._autoscroll()

    def _autoscroll(self):
        self.root.update_idletasks()
        try:
            self.canvas.yview_moveto(1.0)
        except Exception:
            pass

    def send_message(self):
        text = self.entry.get().strip()
        if not text or text == "How may i help you ?":
            return

        # Add user message
        self._add_user_message(text)
        self.entry.delete(0, tk.END)

        # Typing indicator
        typing = tk.Label(self.scrollable, text="...", bg="white", fg="#222222", font=("Arial", 12))
        typing.pack(anchor="w", padx=18, pady=6)
        self._autoscroll()

        # Run AI call in thread
        threading.Thread(target=self._get_response, args=(text, typing), daemon=True).start()

    def _get_response(self, text, typing_widget):
        response = process_command(text)

        # Update GUI from main thread
        self.root.after(0, lambda: self._display_response(response, typing_widget))

    def _display_response(self, response, typing_widget):
        typing_widget.destroy()
        self._add_bot_message(response)


def run_gui():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()


if __name__ == '__main__':
    run_gui()
