import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFormLayout,
                             QStackedWidget, QHBoxLayout, QMessageBox, QSlider, QTabWidget, QFileDialog, QGridLayout)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class LoginRegisterUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Smart Home System')
        self.setGeometry(100, 100, 400, 300)

        self.stack = QStackedWidget(self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stack)

        self.login_widget = QWidget()
        self.register_widget = QWidget()

        self.init_login_ui()
        self.init_register_ui()

        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.register_widget)

    def init_login_ui(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.login_username = QLineEdit()
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.Password)
        form_layout.addRow('Username:', self.login_username)
        form_layout.addRow('Password:', self.login_password)
        layout.addLayout(form_layout)

        login_button = QPushButton('Login')
        login_button.clicked.connect(self.login)
        register_button = QPushButton('Register')
        register_button.clicked.connect(self.show_register)

        login_button.setStyleSheet("background-color: #4CAF50; color: white;")
        register_button.setStyleSheet("background-color: #2196F3; color: white;")

        layout.addWidget(login_button)
        layout.addWidget(register_button)
        self.login_widget.setLayout(layout)

    def init_register_ui(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.register_username = QLineEdit()
        self.register_password = QLineEdit()
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_confirm_password = QLineEdit()
        self.register_confirm_password.setEchoMode(QLineEdit.Password)
        form_layout.addRow('Username:', self.register_username)
        form_layout.addRow('Password:', self.register_password)
        form_layout.addRow('Confirm Password:', self.register_confirm_password)
        layout.addLayout(form_layout)

        register_button = QPushButton('Register')
        register_button.clicked.connect(self.register)
        back_button = QPushButton('Back to Login')
        back_button.clicked.connect(self.show_login)

        register_button.setStyleSheet("background-color: #4CAF50; color: white;")
        back_button.setStyleSheet("background-color: #2196F3; color: white;")

        layout.addWidget(register_button)
        layout.addWidget(back_button)
        self.register_widget.setLayout(layout)

    def show_login(self):
        self.stack.setCurrentWidget(self.login_widget)

    def show_register(self):
        self.stack.setCurrentWidget(self.register_widget)

    def login(self):
        QMessageBox.information(self, 'Login', 'Login Successful')
        self.close()
        self.main_ui = MainUI()
        self.main_ui.show()

    def register(self):
        if self.register_password.text() != self.register_confirm_password.text():
            QMessageBox.warning(self, 'Error', 'Passwords do not match')
        else:
            QMessageBox.information(self, 'Register', 'Registration Successful')
            self.show_login()


class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Smart Home Control Panel')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_home_tab(), "Home")
        self.tabs.addTab(self.create_devices_tab(), "Devices")
        self.tabs.addTab(self.create_environment_tab(), "Environment")
        self.tabs.addTab(self.create_object_recognition_tab(), "Object Recognition")
        self.tabs.addTab(self.create_user_tab(), "User")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def create_home_tab(self):
        home_widget = QWidget()
        layout = QVBoxLayout()
        overlay_layout = QVBoxLayout()

        home_image = QLabel()
        pixmap = QPixmap('/Users/liuyukai/Desktop/smart.jpeg')  # Replace with your image path
        home_image.setPixmap(pixmap)
        home_image.setScaledContents(True)
        home_image.setFixedSize(800, 600)
        layout.addWidget(home_image)

        welcome_label = QLabel('Welcome to Smart Home System')
        welcome_label.setStyleSheet("font-size: 24px; color: white; background-color: rgba(0, 0, 0, 128);")
        welcome_label.setAlignment(Qt.AlignCenter)
        overlay_layout.addWidget(welcome_label, alignment=Qt.AlignCenter)

        home_widget.setLayout(layout)
        home_image.setLayout(overlay_layout)
        return home_widget
    def create_devices_tab(self):
        devices_widget = QWidget()
        layout = QGridLayout()

        home_button = QPushButton('Home')
        movie_button = QPushButton('Movie')
        sleep_button = QPushButton('Sleep')
        away_button = QPushButton('Away')
        lights_button = QPushButton('Lights')
        windows_button = QPushButton('Windows')

        home_button.setStyleSheet("background-color: #FFFFFF;")
        movie_button.setStyleSheet("background-color: #FFFFFF;")
        sleep_button.setStyleSheet("background-color: #FFFFFF;")
        away_button.setStyleSheet("background-color: #FFFFFF;")
        lights_button.setStyleSheet("background-color: #FFFFFF;")
        windows_button.setStyleSheet("background-color: #FFFFFF;")

        layout.addWidget(home_button, 0, 0)
        layout.addWidget(movie_button, 0, 1)
        layout.addWidget(sleep_button, 1, 0)
        layout.addWidget(away_button, 1, 1)
        layout.addWidget(lights_button, 2, 0)
        layout.addWidget(windows_button, 2, 1)

        lights_button.clicked.connect(self.show_lights_status)

        devices_widget.setLayout(layout)
        return devices_widget

    def show_lights_status(self):
        self.lights_status_ui = LightsStatusUI()
        self.lights_status_ui.show()

    def create_environment_tab(self):
        env_widget = QWidget()
        layout = QVBoxLayout()

        temp_label = QLabel('Temperature: 24°C')
        hum_label = QLabel('Humidity: 46%')

        layout.addWidget(temp_label)
        layout.addWidget(hum_label)

        env_widget.setLayout(layout)
        return env_widget

    def create_object_recognition_tab(self):
        object_recognition_widget = QWidget()
        layout = QVBoxLayout()

        self.upload_button = QPushButton('Upload Image')
        self.upload_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.upload_button.clicked.connect(self.upload_image)
        self.result_label = QLabel('Recognition Result: None')

        layout.addWidget(self.upload_button)
        layout.addWidget(self.result_label)

        object_recognition_image = QLabel()
        pixmap = QPixmap('path_to_object_recognition_image.jpg')  # Replace with your image path
        object_recognition_image.setPixmap(pixmap)
        layout.addWidget(object_recognition_image)

        object_recognition_widget.setLayout(layout)
        return object_recognition_widget

    def upload_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Image Files (*.png *.jpg *.bmp)')
        if file_name:
            recognition_result = "Object recognized: Example Object"
            self.result_label.setText(f'Recognition Result: {recognition_result}')

    def create_user_tab(self):
        user_widget = QWidget()
        layout = QVBoxLayout()

        user_info_layout = QFormLayout()
        self.user_name = QLabel('John Doe')
        self.user_email = QLabel('john.doe@example.com')
        user_info_layout.addRow('Name:', self.user_name)
        user_info_layout.addRow('Email:', self.user_email)
        layout.addLayout(user_info_layout)

        user_image = QLabel()
        pixmap = QPixmap('path_to_user_image.jpg')  # Replace with your image path
        user_image.setPixmap(pixmap)
        layout.addWidget(user_image)

        logout_button = QPushButton('Logout')
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

        user_widget.setLayout(layout)
        return user_widget

    def logout(self):
        QMessageBox.information(self, 'Logout', 'Logged out successfully')
        self.close()
        self.open_login_ui()

    def open_login_ui(self):
        self.login_ui = LoginRegisterUI()
        self.login_ui.show()

class LightsStatusUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Lights Status')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.status_label = QLabel('Lights are currently OFF')
        self.status_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(self.status_label, alignment=Qt.AlignCenter)

        self.toggle_button = QPushButton('Toggle Lights')
        self.toggle_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.toggle_button.clicked.connect(self.toggle_lights)
        layout.addWidget(self.toggle_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def toggle_lights(self):
        if self.status_label.text() == 'Lights are currently OFF':
            self.status_label.setText('Lights are currently ON')
            self.toggle_button.setStyleSheet("background-color: #F44336; color: white;")
        else:
            self.status_label.setText('Lights are currently OFF')
            self.toggle_button.setStyleSheet("background-color: #4CAF50; color: white;")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_ui = LoginRegisterUI()
    login_ui.show()
    sys.exit(app.exec_())