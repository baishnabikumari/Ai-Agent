from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QScrollArea, QFrame
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from Backend.Assistant import process_command
import sys


class ChatBubble(QLabel):
    def __init__(self, text, is_user=False):
        super().__init__(text)
        self.setWordWrap(True)
        self.setMargin(10)
        self.setStyleSheet(
            """
            QLabel {
                border-radius: 15px;
                padding: 10px;
            }
            """
        )
        if is_user:
            self.setStyleSheet(
                """
                QLabel {
                    background-color: #DCF8C6;
                    color: black;
                    border-radius: 15px;
                    padding: 10px;
                }
                """
            )
        else:
            self.setStyleSheet(
                """
                QLabel {
                    background-color: #FFFFFF;
                    color: black;
                    border-radius: 15px;
                    padding: 10px;
                }
                """
            )


class JarvisApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis AI")
        self.setGeometry(200, 100, 450, 600)
        self.setStyleSheet("background-color: #F5F5F5;")

        # Main layout
        layout = QVBoxLayout(self)

        # Logo + Title
        header = QLabel()
        pixmap = QPixmap("Frontend/graphic/jarvis.gif")
        pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        header.setPixmap(pixmap)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Jarvis AI\n<small><i>Online</i></small>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))

        layout.addWidget(header)
        layout.addWidget(title)

        # Chat area with scroll
        self.chat_area = QVBoxLayout()
        self.chat_area.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setLayout(self.chat_area)
        scroll.setWidget(scroll_content)

        layout.addWidget(scroll)

        # Input field
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("How may I help you?")
        self.input_field.returnPressed.connect(self.send_message)

        send_btn = QPushButton("➤")
        send_btn.setFixedWidth(50)
        send_btn.clicked.connect(self.send_message)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(send_btn)
        layout.addLayout(input_layout)

    def send_message(self):
        user_text = self.input_field.text().strip()
        if not user_text:
            return

        # Add user bubble
        self.chat_area.addWidget(ChatBubble(user_text, is_user=True))

        # Process AI response
        bot_response = process_command(user_text)
        self.chat_area.addWidget(ChatBubble(bot_response, is_user=False))

        # Clear input
        self.input_field.clear()


# ✅ Run GUI function
def run_gui():
    app = QApplication(sys.argv)
    window = JarvisApp()
    window.show()
    sys.exit(app.exec())
