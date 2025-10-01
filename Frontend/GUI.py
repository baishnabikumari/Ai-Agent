import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from Backend.Assistant import process_command


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis AI")
        self.setGeometry(300, 100, 450, 650)

        # --- Main Layout ---
        main_layout = QVBoxLayout(self)

        # --- Logo + Title ---
        self.logo_label = QLabel()
        pixmap = QPixmap("Frontend/graphic/jarvis_logo.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel("Jarvis AI\n<small><i>Online</i></small>")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")

        main_layout.addWidget(self.logo_label)
        main_layout.addWidget(self.title_label)

        # --- Chat Area ---
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("""
            QTextEdit {
                background-color: #2e2e2e;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        main_layout.addWidget(self.chat_area, stretch=1)

        # --- Input + Button ---
        input_layout = QHBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("How may I help you?")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                border: 1px solid #555;
                border-radius: 12px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("➤")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #3a86ff;
                color: white;
                border-radius: 12px;
                font-size: 16px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #266dd3;
            }
        """)
        self.send_button.clicked.connect(self.send_message)

        input_layout.addWidget(self.input_field, stretch=1)
        input_layout.addWidget(self.send_button)

        main_layout.addLayout(input_layout)

        # --- Dark Theme ---
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
                font-family: 'Segoe UI', sans-serif;
            }
        """)

    def send_message(self):
        user_text = self.input_field.text().strip()
        if not user_text:
            return

        # Show user message
        self.chat_area.append(f"<p style='background:#4caf50; padding:8px; border-radius:8px; color:black;'><b>You:</b> {user_text}</p>")

        # Get Jarvis response
        bot_response = process_command(user_text)

        # Show bot response
        self.chat_area.append(f"<p style='background:#2e2e2e; padding:8px; border-radius:8px;'><b>Jarvis:</b> {bot_response}</p>")

        # Scroll to bottom
        self.chat_area.verticalScrollBar().setValue(self.chat_area.verticalScrollBar().maximum())

        # Clear input
        self.input_field.clear()


def run_gui():
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_gui()
