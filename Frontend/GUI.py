from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QLineEdit, QTextBrowser, QComboBox, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QMovie, QFont, QColor, QTextCursor
from PyQt5.QtCore import Qt
from Backend.Assistant import process_command


class ChatBubble(QLabel):
    """Custom chat bubble with styles"""
    def __init__(self, text, is_user=True):
        super().__init__(text)
        self.setWordWrap(True)
        self.setFont(QFont("Arial", 11))
        self.setMargin(10)
        self.setStyleSheet(
            "QLabel {"
            f"background-color: {'#1E88E5' if is_user else '#2E2E2E'};"
            f"color: {'white' if is_user else '#E0E0E0'};"
            "border-radius: 12px;"
            "padding: 8px;"
            "}"
        )


class JarvisApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis AI")
        self.setGeometry(200, 200, 700, 600)
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()

        # Jarvis Animation Header
        self.gif_label = QLabel(alignment=Qt.AlignCenter)
        movie = QMovie("Frontend/graphics/jarvis.gif")
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label)

        # Mode Selector
        mode_layout = QHBoxLayout()
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["auto", "openai", "groq"])
        self.mode_selector.setStyleSheet(
            "QComboBox { background-color: #2E2E2E; color: white; padding: 6px; border-radius: 8px; }"
        )
        mode_layout.addWidget(QLabel("Mode:"))
        mode_layout.addWidget(self.mode_selector)
        layout.addLayout(mode_layout)

        # Chat Display (scrollable text area)
        self.chat_display = QTextBrowser()
        self.chat_display.setStyleSheet(
            "QTextBrowser { background-color: #1E1E1E; border: none; padding: 10px; border-radius: 10px; }"
        )
        layout.addWidget(self.chat_display, stretch=1)

        # Input Layout
        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message to Jarvis...")
        self.input_box.setStyleSheet(
            "QLineEdit { background-color: #2E2E2E; border-radius: 12px; padding: 10px; color: white; }"
        )
        input_layout.addWidget(self.input_box)

        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet(
            "QPushButton { background-color: #1E88E5; color: white; padding: 10px; border-radius: 12px; }"
            "QPushButton:hover { background-color: #1565C0; }"
        )
        self.send_button.clicked.connect(self.handle_chat)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)

        self.setLayout(layout)

    def handle_chat(self):
        user_input = self.input_box.text().strip()
        if not user_input:
            return

        # Display user message
        self.chat_display.append(f"<p style='text-align:right; color:#90CAF9;'><b>You:</b> {user_input}</p>")
        self.input_box.clear()

        # Get AI Response
        mode = self.mode_selector.currentText()
        response = process_command(user_input, mode=mode)

        # Display Jarvis response
        self.chat_display.append(f"<p style='text-align:left; color:#A5D6A7;'><b>Jarvis:</b> {response}</p>")
        self.chat_display.moveCursor(QTextCursor.End)


def run_gui():
    app = QApplication([])
    jarvis = JarvisApp()
    jarvis.show()
    app.exec_()
