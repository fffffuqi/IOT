import subprocess
import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QStackedWidget, QTabWidget,
                             QLabel, QFileDialog, QGridLayout, QMessageBox, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from services import UserService
from controllers import UserController, EnvironmentController

def ensure_numpy_installed():
    try:
        import numpy as np
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
        import numpy as np

ensure_numpy_installed()

class LoginRegisterUI(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = UserController(self)
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
        login_button.clicked.connect(self.controller.login)
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
        register_button.clicked.connect(self.controller.register)
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

    def show_main_ui(self):
        try:
            self.main_ui = MainUI(controller=self.controller)
            self.main_ui.show()
            self.close()
        except Exception as e:
            print(f"Error in show_main_ui: {e}")
            QMessageBox.critical(self, "Error", "Failed to open the main UI. Please try again.")

class MainUI(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
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

        home_image = QLabel()
        try:
            pixmap = QPixmap('C:/Users/17590/PycharmProjects/onnxcaffe/static/smart.png')
            home_image.setPixmap(pixmap)
        except Exception as e:
            print(f"Error loading image: {e}")
            home_image.setText("Error loading image")
        home_image.setScaledContents(True)
        home_image.setFixedSize(800, 600)
        layout.addWidget(home_image)

        home_widget.setLayout(layout)
        return home_widget

    def create_devices_tab(self):
        devices_widget = QWidget()
        layout = QGridLayout()

        controls = [
            ('Door', 'Doors are currently CLOSED'),
            ('Alert', 'Alerts are currently OFF'),
            ('Curtain', 'Curtains are currently CLOSED'),
            ('Aircondition', 'Aircondition is currently OFF'),
            ('Lights', 'Lights are currently OFF'),
            ('Windows', 'Windows are currently CLOSED')
        ]

        self.status_labels = {}
        self.buttons = {}

        for i, control in enumerate(controls):
            button = QPushButton(control[0])
            button.setStyleSheet("background-color: #4CAF50; color: white;")
            button.clicked.connect(lambda _, b=button, t=control[1]: self.toggle_status(b, t))
            layout.addWidget(button, i // 2, i % 2)

            label = QLabel(control[1])
            label.setStyleSheet("font-size: 18px;")
            layout.addWidget(label, i // 2 + 3, i % 2)

            self.status_labels[button.text()] = label
            self.buttons[button.text()] = button

        devices_widget.setLayout(layout)
        return devices_widget

    def toggle_status(self, button, initial_text):
        label = self.status_labels[button.text()]
        if label.text().endswith('OFF') or label.text().endswith('CLOSED'):
            label.setText(label.text().replace('OFF', 'ON').replace('CLOSED', 'OPEN'))
            button.setStyleSheet("background-color: #F44336; color: white;")
        else:
            label.setText(initial_text)
            button.setStyleSheet("background-color: #4CAF50; color: white;")

    def create_environment_tab(self):
        env_widget = QWidget()
        layout = QVBoxLayout()

        self.env_table = QTableWidget(8, 5)
        self.env_table.setHorizontalHeaderLabels(['time', 'temperature', 'lighting', 'Doorswitch', 'Windowswitch'])

        self.env_controller = EnvironmentController(self)
        self.env_controller.populate_env_table(1)

        self.env_last_page_button = QPushButton('Last Page')
        self.env_last_page_button.clicked.connect(self.env_controller.show_env_last_page)

        self.env_next_page_button = QPushButton('Next Page')
        self.env_next_page_button.clicked.connect(self.env_controller.show_env_next_page)

        self.env_page_num_label = QLabel('Page: 1')
        self.env_current_page = 1

        self.env_table.setCellWidget(7, 0, self.env_last_page_button)
        self.env_table.setCellWidget(7, 4, self.env_next_page_button)
        self.env_table.setCellWidget(7, 2, self.env_page_num_label)

        self.env_table.itemChanged.connect(self.env_controller.update_env_data)

        layout.addWidget(self.env_table)
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

        self.yolo_detect_button = QPushButton('YOLO Detect')
        self.yolo_detect_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.yolo_detect_button.clicked.connect(self.yolo_detect)

        layout.addWidget(self.yolo_detect_button)

        self.enter_facial_data_button = QPushButton('Enter facial data')
        self.enter_facial_data_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.enter_facial_data_button.clicked.connect(self.enter_facial_data)

        layout.addWidget(self.enter_facial_data_button)

        object_recognition_image = QLabel()
        try:
            pixmap = QPixmap('image.jpg')
            object_recognition_image.setPixmap(pixmap)
        except Exception as e:
            print(f"Error loading object recognition image: {e}")
            object_recognition_image.setText("Error loading image")
        layout.addWidget(object_recognition_image)

        object_recognition_widget.setLayout(layout)
        return object_recognition_widget

    def upload_image(self):
        try:
            subprocess.run([sys.executable, 'C:\\Users\\17590\\PycharmProjects\\onnxcaffe\\onnxcaffe.py'], check=True)
            self.result_label.setText('Recognition Result: Script Executed')
        except subprocess.CalledProcessError as e:
            print(f"Error executing script: {e}")
            self.result_label.setText(f'Recognition Result: Error {str(e)}')

    def yolo_detect(self):
        try:
            subprocess.run([sys.executable, 'C:\\Users\\17590\\PycharmProjects\\onnxcaffe\\yolofacedetect.py'], check=True)
            self.result_label.setText('YOLO Detection Result: Script Executed')
        except subprocess.CalledProcessError as e:
            print(f"Error executing YOLO detection script: {e}")
            self.result_label.setText(f'YOLO Detection Result: Error {str(e)}')

    def enter_facial_data(self):
        try:
            subprocess.run([sys.executable, 'C:\\Users\\17590\\PycharmProjects\\onnxcaffe\\Enterfacialdata.py'], check=True)
            self.result_label.setText('Enter Facial Data Result: Script Executed')
        except subprocess.CalledProcessError as e:
            print(f"Error executing Enter Facial Data script: {e}")
            self.result_label.setText(f'Enter Facial Data Result: Error {str(e)}')

    def create_user_tab(self):
        user_widget = QWidget()
        layout = QVBoxLayout()

        user_info_layout = QFormLayout()
        online_user = UserService.get_online_user()  # 从 UserService 获取在线用户
        if online_user:
            self.user_name = QLabel(online_user[0])
            self.auth_status = QLabel('Already Verified' if online_user[1] else 'Not Verified')
        else:
            self.user_name = QLabel('Unknown')
            self.auth_status = QLabel('Not Verified')

        user_info_layout.addRow('Name:', self.user_name)
        user_info_layout.addRow('Status:', self.auth_status)
        layout.addLayout(user_info_layout)

        self.user_table = QTableWidget(8, 5)
        self.user_table.setHorizontalHeaderLabels(['userid', 'password', 'authentic', 'auntheninfo', 'online'])
        self.populate_user_table(1)

        self.last_page_button = QPushButton('Last Page')
        self.last_page_button.clicked.connect(self.show_last_page)

        self.next_page_button = QPushButton('Next Page')
        self.next_page_button.clicked.connect(self.show_next_page)

        self.page_num_label = QLabel('Page: 1')
        self.current_page = 1

        self.user_table.setCellWidget(7, 0, self.last_page_button)
        self.user_table.setCellWidget(7, 4, self.next_page_button)
        self.user_table.setCellWidget(7, 2, self.page_num_label)

        self.user_table.itemChanged.connect(self.update_user_data)

        layout.addWidget(self.user_table)
        layout.addWidget(QPushButton('Logout', clicked=self.logout))
        user_widget.setLayout(layout)
        return user_widget

    def populate_user_table(self, page_num):
        try:
            users = UserService.get_users_by_page(page_num, 6)
            for row in range(6):
                if row < len(users):
                    for col, value in enumerate(users[row]):
                        item = QTableWidgetItem(str(value))
                        if col < 3:
                            item.setFlags(item.flags() | Qt.ItemIsEditable)
                        self.user_table.setItem(row + 1, col, item)
                else:
                    for col in range(5):
                        self.user_table.setItem(row + 1, col, QTableWidgetItem(""))
        except Exception as e:
            print(f"Error populating user table: {e}")
            QMessageBox.critical(self, "Error", "Failed to populate user table.")

    def show_last_page(self):
        try:
            if self.current_page > 1:
                self.current_page -= 1
                self.populate_user_table(self.current_page)
                self.page_num_label.setText(f'Page: {self.current_page}')
        except Exception as e:
            print(f"Error showing last page: {e}")

    def show_next_page(self):
        try:
            self.current_page += 1
            users = UserService.get_users_by_page(self.current_page, 6)
            if users:
                self.populate_user_table(self.current_page)
                self.page_num_label.setText(f'Page: {self.current_page}')
            else:
                self.current_page -= 1
        except Exception as e:
            print(f"Error showing next page: {e}")

    def update_user_data(self, item):
        try:
            row = item.row()
            col = item.column()
            if 1 <= row <= 6 and col < 3:
                value = item.text()
                if col == 0 and (0 < len(value) < 15):
                    UserService.update_user(self.user_table.item(row, 0).text(), 'userid', value)
                elif col == 1 and (0 < len(value) < 15):
                    UserService.update_user(self.user_table.item(row, 0).text(), 'password', value)
                elif col == 2 and value in ['0', '1']:
                    UserService.update_user(self.user_table.item(row, 0).text(), 'authentic', int(value))
                else:
                    item.setText('Invalid')
        except Exception as e:
            print(f"Error updating user data: {e}")
            QMessageBox.critical(self, "Error", "Failed to update user data.")

    def logout(self):
        try:
            if self.controller:
                self.controller.logout()
            self.open_login_ui()
        except Exception as e:
            print(f"Error during logout: {e}")
            QMessageBox.critical(self, "Error", "Failed to logout. Please try again.")

    def open_login_ui(self):
        try:
            self.login_ui = LoginRegisterUI()
            self.login_ui.show()
            self.close()
        except Exception as e:
            print(f"Error opening login UI: {e}")
            QMessageBox.critical(self, "Error", "Failed to open login UI. Please try again.")
