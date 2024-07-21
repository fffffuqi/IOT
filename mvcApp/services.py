from models import UserModel, EnvironmentModel

class UserService:
    @staticmethod
    def register_user(username, password, confirm_password):
        if not username or not password or not confirm_password:
            return "Inputs cannot be empty"
        if len(username) > 20 or len(password) > 20:
            return "Inputs too long"
        if password != confirm_password:
            return "Passwords do not match"
        if UserModel.get_user_by_id(username):
            return "Username already exists"
        try:
            UserModel.create_user(username, password)
            return "Registration Successful"
        except Exception as e:
            print(f"Error in register_user: {e}")
            return "Registration Failed"

    @staticmethod
    def authenticate_user(username, password):
        try:
            user = UserModel.get_user_by_id(username)
            if user and user[1] == password:
                UserModel.set_user_online(username, True)
                return True
            return False
        except Exception as e:
            print(f"Error in authenticate_user: {e}")
            return False

    @staticmethod
    def logout_user():
        try:
            UserModel.set_all_users_offline()
        except Exception as e:
            print(f"Error in logout_user: {e}")

    @staticmethod
    def get_online_user():
        try:
            return UserModel.get_online_user()
        except Exception as e:
            print(f"Error in get_online_user: {e}")
            return None

    @staticmethod
    def get_users_by_page(page_num, page_size):
        try:
            return UserModel.get_users_by_page(page_num, page_size)
        except Exception as e:
            print(f"Error in get_users_by_page: {e}")
            return []

    @staticmethod
    def update_user(userid, field, value):
        try:
            UserModel.update_user(userid, field, value)
        except Exception as e:
            print(f"Error in update_user: {e}")

class EnvironmentService:
    @staticmethod
    def get_environment_data_by_page(page_num, page_size):
        try:
            return EnvironmentModel.get_data_by_page(page_num, page_size)
        except Exception as e:
            print(f"Error in get_environment_data_by_page: {e}")
            return []

    @staticmethod
    def update_environment_data(time, field, value):
        try:
            EnvironmentModel.update_data(time, field, value)
        except Exception as e:
            print(f"Error in update_environment_data: {e}")
