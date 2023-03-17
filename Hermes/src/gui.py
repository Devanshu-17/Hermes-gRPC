import sys
from datetime import datetime
from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QInputDialog,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox
)
from main_client import ChatClient


class ChatGUI(QWidget):
    def __init__(self, client, username):
        super().__init__()
        self.client = client
        self.messages = []
        self.username = username
        self.last_login = "Never"
        self.update_messages_timer = self.startTimer(1000)  # call update_messages every 1000 milliseconds (1 second)
        self.setStyleSheet("background-color: #6670DD;")

        self.setWindowTitle("HERMES")
        self.setGeometry(0, 0, 1200, 800)

        # Create UI elements
        self.logo_label = QLabel(self)
        self.logo_pixmap = QPixmap('.././assets/logo.png')
        self.logo_pixmap = self.logo_pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio)  
        self.logo_label.setPixmap(self.logo_pixmap)

        self.title_label = QLabel("Hermes", self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 40px;")
        self.title_label.setFont(QtGui.QFont("Apple Chancery"))

        self.username_label = QLabel(f"Username: {self.username}")
        self.username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.username_label.setStyleSheet("font-size: 30px;")
        self.username_label.setFont(QtGui.QFont("Georgia"))

        self.last_login_label = QLabel(f"Last login: {self.last_login}")
        self.last_login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.last_login_label.setStyleSheet("font-size: 30px;")
        self.last_login_label.setFont(QtGui.QFont("Georgia"))

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.on_closing)
        self.logout_button.setFixedWidth(100)
        self.logout_button.setStyleSheet("font-size: 24px; background-color: black; color: white;")
        self.logout_button.setFont(QtGui.QFont("Georgia"))



        profile_layout = QVBoxLayout()
        profile_layout.addWidget(self.logo_label)
        profile_layout.addWidget(self.title_label)
        # profile_layout.addWidget(self.profile_label)
        profile_layout.addWidget(self.username_label)
        profile_layout.addWidget(self.last_login_label)
        profile_layout.addWidget(self.logout_button)

        profile_widget = QWidget()
        profile_widget.setLayout(profile_layout)
        profile_widget.setStyleSheet("background-color: #0B1C76;")
 
        self.chat_label = QLabel("Chat Messages:")
        self.chat_label.setStyleSheet("font-size: 24px;")
        self.chat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        chat_stylesheet = "background-color: #0B1C76; font-size: 20px;"
        self.chat_listbox = QListWidget()
        self.chat_listbox.setStyleSheet(chat_stylesheet)
        self.chat_listbox.setFixedSize(800, 800)

        chat_layout = QVBoxLayout()
        chat_layout.addWidget(self.chat_label)
        chat_layout.addWidget(self.chat_listbox)
        chat_widget = QWidget()
        chat_widget.setLayout(chat_layout)
        # chat_widget.setStyleSheet("background-color: #1dc8d7;")
        chat_widget.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b198a, stop:1 #1dc8d7);")

        self.message_label = QLabel("Message:")
        self.message_label.setFont(QtGui.QFont("Georgia"))
        self.message_label.setStyleSheet("font-size: 24px;")
        self.message_entry = QLineEdit()
        self.message_entry.setStyleSheet("background-color: black;")
        self.message_entry.setFixedWidth(200)
        self.send_button = QPushButton("Send")
        self.send_button.setFont(QtGui.QFont("Georgia"))
        self.send_button.setStyleSheet("font-size: 20px; background-color: #0B1C76; color: white;")
        self.send_button.setFixedWidth(100)
        self.send_button.clicked.connect(self.send_message)

        message_layout = QHBoxLayout()
        message_layout.addWidget(self.message_label)
        message_layout.addWidget(self.message_entry)
        message_layout.addWidget(self.send_button)


        # Main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(profile_widget)
        main_layout.addWidget(chat_widget)
        main_layout.addLayout(message_layout)

        self.setLayout(main_layout)

        self.update_profile()
        self.update_messages()


    def timerEvent(self, event):
        if event.timerId() == self.update_messages_timer:
            self.update_messages()
        elif event.timerId() == self.update_profile_timer:
            self.update_profile()
        else:
            super().timerEvent(event)

    def set_username(self, username):
        self.username = username
        self.username_label.setText(f"Username: {self.username}")

    def send_message(self):
        content = self.message_entry.text()

        if content:
            response = self.client.send_message(self.username, content)
            self.message_entry.clear()
            # Add the sent message to the chat listbox
            message = f"{self.username}: {content}"
            self.chat_listbox.addItem(message)

    def update_messages(self):
        messages = list(self.client.receive_messages())

        # Clear the messages list before appending the new messages
        self.messages.clear()

        # Add all messages (including the "user left" message) to the chat listbox
        self.chat_listbox.clear()
        for message in messages:
            self.messages.append(message)
            item = QListWidgetItem(message)
            if "<left>" in message:
                item.setForeground(QtGui.QBrush(QtGui.QColor("red")))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.chat_listbox.addItem(item)

        self.update_messages_timer = self.startTimer(1000)




    def update_profile(self):
        self.last_login = datetime.now().strftime("%H:%M")

        self.last_login_label.setText(f"Last login: {self.last_login}")
        self.update_profile_timer = self.startTimer(60000)

    def on_closing(self):
        # Inform the server that the user is leaving
        self.client.send_message(self.username, "<left>")

        # Add a message to the chat listbox indicating that the user has left
        message = f"{self.username} has left the chat"
        item = QListWidgetItem(message)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setForeground(QtGui.QBrush(QtGui.QColor("red")))
        self.chat_listbox.addItem(item)

        # Refresh the message list to show that the user has left
        self.update_messages()

        # Print a message indicating that the user has left the chat
        print(f"{self.username} has left the chat")

        # Close the window
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = ChatClient()
    username, ok = QInputDialog.getText(None, "Username", "Enter username:")
    if ok:
        gui = ChatGUI(client, username)
        gui.show()
        sys.exit(app.exec())
