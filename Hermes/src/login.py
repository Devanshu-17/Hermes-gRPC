from PyQt6.QtWidgets import QApplication, QFrame, QFormLayout, QHBoxLayout, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QFileDialog
from PyQt6 import QtGui, QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from pymongo import MongoClient
from gui import ChatGUI
from main_client import ChatClient
import bcrypt


class LoginPage(QMainWindow):
    def __init__(self):
        super().__init__()

        # set window title and size
        self.setWindowTitle("Login")
        self.setFixedSize(800, 800)

        # set up central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        hbox = QHBoxLayout()
        central_widget.setLayout(hbox)

        # set up left sidebar
        left_sidebar = QFrame()
        left_sidebar.setFixedWidth(400)
        left_sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        hbox.addWidget(left_sidebar)

        left_vbox = QVBoxLayout()
        left_sidebar.setLayout(left_vbox)

        # add logo and app title to sidebar
        logo_label = QLabel()
        logo_pixmap = QPixmap(".././assets/logo.png")
        logo_pixmap = logo_pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio)
        #center logo
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setPixmap(logo_pixmap)
        left_vbox.addWidget(logo_label)

        title_label = QLabel("Hermes")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QtGui.QFont("Apple Chancery"))
        title_label.setStyleSheet("font-size: 50px;")
        left_vbox.addWidget(title_label)

        subtitle_label = QLabel("Bringing people together,")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setFont(QtGui.QFont("Georgia"))
        subtitle_label.setStyleSheet("font-size: 20px;")
        left_vbox.addWidget(subtitle_label)

        subtitle_label_1 = QLabel("One message at a time")
        subtitle_label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label_1.setFont(QtGui.QFont("Georgia"))
        subtitle_label_1.setStyleSheet("font-size: 20px;")
        left_vbox.addWidget(subtitle_label_1)

        #add #0B1C76 color to sidebar
        left_sidebar.setStyleSheet("background-color: #0B1C76;")

        # set up login form on right side
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox.addLayout(right_layout)

        central_widget.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b198a, stop:1 #1dc8d7);")

        self.label_username = QLabel("Username:")
        self.label_username.setFont(QtGui.QFont("Georgia"))
        self.label_username.setStyleSheet("font-size: 20px;")
        right_layout.addWidget(self.label_username, alignment=Qt.AlignmentFlag.AlignLeft)

        right_layout.addSpacing(30)

        self.entry_username = QLineEdit()
        self.entry_username.setStyleSheet("background-color: black;")
        self.entry_username.setFixedWidth(200)
        right_layout.addWidget(self.entry_username, alignment=Qt.AlignmentFlag.AlignLeft)


        #add some space between username and password
        right_layout.addSpacing(50)


        self.label_password = QLabel("Password:")
        self.label_password.setFont(QtGui.QFont("Georgia"))
        self.label_password.setStyleSheet("font-size: 20px;")
        right_layout.addWidget(self.label_password, alignment=Qt.AlignmentFlag.AlignLeft)

        right_layout.addSpacing(30)

        self.entry_password = QLineEdit()
        self.entry_password.setFixedWidth(200)
        self.entry_password.setStyleSheet("background-color: black;")
        self.entry_password.setEchoMode(QLineEdit.EchoMode.Password)
        right_layout.addWidget(self.entry_password, alignment=Qt.AlignmentFlag.AlignLeft)

        right_layout.addSpacing(50)

        
        button_layout = QHBoxLayout()
        right_layout.addLayout(button_layout)

        self.logbtn = QPushButton("Login", clicked=self._login_btn_clicked)
        self.logbtn.setFont(QtGui.QFont("Georgia"))
        #change color of login button to black and font to white overriding stylesheet
        self.logbtn.setStyleSheet("font-size: 24px; background-color: #0B1C76; color: white;")
        button_layout.addWidget(self.logbtn)

        self.regbtn = QPushButton("Register", clicked=self._register_btn_clicked)
        self.regbtn.setFont(QtGui.QFont("Georgia"))
        self.regbtn.setStyleSheet("font-size: 24px; background-color: #0B1C76; color: white;")
        button_layout.addWidget(self.regbtn)

        self.client = MongoClient("") //ADD YOUR MONGODB URI HERE
        self.db = self.client["chat_app_db"]
        self.users = self.db["users"]

        # Create ChatClient and ChatGUI instances
        self.chat_client = ChatClient()
        self.chat_gui = ChatGUI(self.chat_client, "")



    def _login_btn_clicked(self):
        username = self.entry_username.text()
        password = self.entry_password.text()

        user = self.users.find_one({"username": username, "password": password})

        if user:
            # Show the ChatGUI instance with the logged in user's username
            self.chat_gui.set_username(username)
            self.chat_gui.show()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Invalid username or password")

    def _register_btn_clicked(self):
        register_page = RegisterPage(self)
        register_page.show()
        
        
        

class RegisterPage(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Register")
        self.setFixedSize(800, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        central_widget.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b198a, stop:1 #1dc8d7);")

        hbox = QHBoxLayout()
        central_widget.setLayout(hbox)

        # set up left sidebar
        left_sidebar = QFrame()
        left_sidebar.setFixedWidth(400)
        left_sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        hbox.addWidget(left_sidebar)

        left_vbox = QVBoxLayout()
        left_sidebar.setLayout(left_vbox)

        # add logo and app title to sidebar
        logo_label = QLabel()
        logo_pixmap = QPixmap(".././assets/logo.png")
        logo_pixmap = logo_pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio)
        #center logo
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setPixmap(logo_pixmap)
        left_vbox.addWidget(logo_label)

        title_label = QLabel("Hermes")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QtGui.QFont("Apple Chancery"))
        title_label.setStyleSheet("font-size: 50px;")
        left_vbox.addWidget(title_label)

        subtitle_label = QLabel("Bringing people together,")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setFont(QtGui.QFont("Georgia"))
        subtitle_label.setStyleSheet("font-size: 20px;")
        left_vbox.addWidget(subtitle_label)

        subtitle_label_1 = QLabel("One message at a time")
        subtitle_label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label_1.setFont(QtGui.QFont("Georgia"))
        subtitle_label_1.setStyleSheet("font-size: 20px;")
        left_vbox.addWidget(subtitle_label_1)

        #add #0B1C76 color to sidebar
        left_sidebar.setStyleSheet("background-color: #0B1C76;")

        # set up registration form on right side
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox.addLayout(right_layout)

        self.label_username = QLabel("Username:")
        self.label_username.setFont(QtGui.QFont("Georgia"))
        self.label_username.setStyleSheet("font-size: 20px;")
        right_layout.addWidget(self.label_username, alignment=Qt.AlignmentFlag.AlignLeft)

        right_layout.addSpacing(30)

        self.entry_username = QLineEdit()
        self.entry_username.setStyleSheet("background-color: black;")
        self.entry_username.setFixedWidth(200)
        right_layout.addWidget(self.entry_username, alignment=Qt.AlignmentFlag.AlignLeft)


        #add some space between username and password
        right_layout.addSpacing(50)


        self.label_password = QLabel("Password:")
        self.label_password.setFont(QtGui.QFont("Georgia"))
        self.label_password.setStyleSheet("font-size: 20px;")
        right_layout.addWidget(self.label_password, alignment=Qt.AlignmentFlag.AlignLeft)

        right_layout.addSpacing(30)

        self.entry_password = QLineEdit()
        self.entry_password.setFixedWidth(200)
        self.entry_password.setStyleSheet("background-color: black;")
        self.entry_password.setEchoMode(QLineEdit.EchoMode.Password)
        right_layout.addWidget(self.entry_password, alignment=Qt.AlignmentFlag.AlignLeft)

        right_layout.addSpacing(50)

          # confirm password input field
        self.label_confirm_password = QLabel("Confirm Password:")
        self.label_confirm_password.setFont(QtGui.QFont("Georgia"))
        self.label_confirm_password.setStyleSheet("font-size: 20px;")
        right_layout.addWidget(self.label_confirm_password, alignment=Qt.AlignmentFlag.AlignLeft)

        right_layout.addSpacing(30)

        self.entry_confirm_password = QLineEdit()
        self.entry_confirm_password.setFixedWidth(200)
        self.entry_confirm_password.setStyleSheet("background-color: black;")
        self.entry_confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        right_layout.addWidget(self.entry_confirm_password, alignment=Qt.AlignmentFlag.AlignLeft)

        # add some space between password and security question
        right_layout.addSpacing(50)

        # # security question input field
        # self.label_security_question = QLabel("Security Question:")
        # self.label_security_question.setFont(QtGui.QFont("Georgia"))
        # self.label_security_question.setStyleSheet("font-size: 20px;")
        # right_layout.addWidget(self.label_security_question, alignment=Qt.AlignmentFlag.AlignLeft)

        # right_layout.addSpacing(30)

        # self.entry_security_question = QLineEdit()
        # self.entry_security_question.setFixedWidth(200)
        # self.entry_security_question.setStyleSheet("background-color: black;")
        # self.entry_security_question.setEchoMode(QLineEdit.EchoMode.Normal)
        # right_layout.addWidget(self.entry_security_question, alignment=Qt.AlignmentFlag.AlignLeft)

        # # # add some space between security question and register button
        # right_layout.addSpacing(50)


        button_layout = QHBoxLayout()
        right_layout.addLayout(button_layout)

        self.regbtn = QPushButton("Register", clicked=self._register_btn_clicked)
        self.regbtn.setFont(QtGui.QFont("Georgia"))
        self.regbtn.setStyleSheet("font-size: 24px; background-color: #0B1C76; color: white;")

        button_layout.addWidget(self.regbtn)


        # self.regbtn = QPushButton("Register", clicked=self._register_btn_clicked)
        # hbox3.addWidget(self.regbtn)

        self.client = MongoClient("") ADD YOUR MONGODB URI HERE
        self.db = self.client["chat_app_db"]
        self.users = self.db["users"]

    def _register_btn_clicked(self):
        username = self.entry_username.text()
        password = self.entry_password.text()
        confirm_password = self.entry_confirm_password.text()
        # security_question = self.entry_security_question.text()

        if not username or not password:
            QMessageBox.critical(self, "Error", "Username and password fields cannot be empty")
        elif self.users.find_one({"username": username}):
            QMessageBox.critical(self, "Error", "Username already exists")
        # elif not security_question:
        #     QMessageBox.critical(self, "Error", "Security question field cannot be empty")
        elif password != confirm_password:
            QMessageBox.critical(self, "Error", "Password and Confirm Password fields should match")
        else:
            # Insert user document into the MongoDB users collection
            # Encrypt password and security question before storing in database
            # salt = bcrypt.gensalt()
            # password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)
            # confirm_password_hash = bcrypt.hashpw(confirm_password.encode("utf-8"), salt)
            # security_question_hash = bcrypt.hashpw(security_question.encode("utf-8"), salt)
            user = {"username": username, "password": password, "confirm_password": confirm_password, "friends": ""}
            self.users.insert_one(user)

            # Show success message and destroy the RegisterPage window
            QMessageBox.information(self, "Success", "Account created successfully")
            self.close()
            login_page = LoginPage()
            login_page.show()



if __name__ == "__main__":
    app = QApplication([])
    login_page = LoginPage()
    login_page.show()
    app.exec()
    
