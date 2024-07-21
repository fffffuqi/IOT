from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from services import UserService, EnvironmentService
from PyQt5.QtCore import Qt

class UserController:
    def __init__(self, view):
        self.view = view

    def login(self):
        try:
            username = self.view.login_username.text()
            password = self.view.login_password.text()
            if UserService.authenticate_user(username, password):
                QMessageBox.information(self.view, 'Login', 'Login Successful')
                self.view.close()
                self.view.show_main_ui()
            else:
                QMessageBox.warning(self.view, 'Error', 'Invalid username or password')
                self.view.login_username.clear()
                self.view.login_password.clear()
        except Exception as e:
            print(f"Error during login: {e}")
            QMessageBox.critical(self.view, 'Error', 'Login failed. Please try again.')

    def register(self):
        try:
            username = self.view.register_username.text()
            password = self.view.register_password.text()
            confirm_password = self.view.register_confirm_password.text()
            result = UserService.register_user(username, password, confirm_password)
            if result == "Registration Successful":
                QMessageBox.information(self.view, 'Register', result)
                self.view.show_login()
            else:
                QMessageBox.warning(self.view, 'Error', result)
            self.view.register_username.clear()
            self.view.register_password.clear()
            self.view.register_confirm_password.clear()
        except Exception as e:
            print(f"Error during registration: {e}")
            QMessageBox.critical(self.view, 'Error', 'Registration failed. Please try again.')

    def logout(self):
        try:
            UserService.logout_user()
            self.view.show_login()
        except Exception as e:
            print(f"Error during logout: {e}")
            QMessageBox.critical(self.view, 'Error', 'Logout failed. Please try again.')

    def get_users_by_page(self, page_num, page_size):
        try:
            return UserService.get_users_by_page(page_num, page_size)
        except Exception as e:
            print(f"Error getting users by page: {e}")
            QMessageBox.critical(self.view, 'Error', 'Failed to get users. Please try again.')
            return []

    def update_user(self, userid, field, value):
        try:
            UserService.update_user(userid, field, value)
        except Exception as e:
            print(f"Error updating user: {e}")
            QMessageBox.critical(self.view, 'Error', 'Failed to update user. Please try again.')

class EnvironmentController:
    def __init__(self, view):
        self.view = view

    def populate_env_table(self, page_num):
        try:
            data = EnvironmentService.get_environment_data_by_page(page_num, 6)
            for row in range(6):
                if row < len(data):
                    for col, value in enumerate(data[row]):
                        item = QTableWidgetItem(str(value))
                        if col < 3:
                            item.setFlags(item.flags() | Qt.ItemIsEditable)
                        self.view.env_table.setItem(row + 1, col, item)
                else:
                    for col in range(5):
                        self.view.env_table.setItem(row + 1, col, QTableWidgetItem(""))
        except Exception as e:
            print(f"Error populating environment table: {e}")
            QMessageBox.critical(self.view, 'Error', 'Failed to populate environment data. Please try again.')

    def show_env_last_page(self):
        try:
            if self.view.env_current_page > 1:
                self.view.env_current_page -= 1
                self.populate_env_table(self.view.env_current_page)
                self.view.env_page_num_label.setText(f'Page: {self.view.env_current_page}')
        except Exception as e:
            print(f"Error showing last page: {e}")
            QMessageBox.critical(self.view, 'Error', 'Failed to show last page. Please try again.')

    def show_env_next_page(self):
        try:
            self.view.env_current_page += 1
            data = EnvironmentService.get_environment_data_by_page(self.view.env_current_page, 6)
            if data:
                self.populate_env_table(self.view.env_current_page)
                self.view.env_page_num_label.setText(f'Page: {self.view.env_current_page}')
            else:
                self.view.env_current_page -= 1
        except Exception as e:
            print(f"Error showing next page: {e}")
            QMessageBox.critical(self.view, 'Error', 'Failed to show next page. Please try again.')

    def update_env_data(self, item):
        try:
            row = item.row()
            col = item.column()
            if 1 <= row <= 6 and col < 3:
                value = item.text()
                field = self.view.env_table.horizontalHeaderItem(col).text().lower()
                EnvironmentService.update_environment_data(self.view.env_table.item(row, 0).text(), field, value)
        except Exception as e:
            print(f"Error updating environment data: {e}")
            QMessageBox.critical(self.view, 'Error', 'Failed to update environment data. Please try again.')
