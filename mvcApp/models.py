import sqlite3

class UserModel:
    @staticmethod
    def get_user_by_id(userid):
        try:
            with sqlite3.connect('C:\\Users\\17590\\PycharmProjects\\onnxcaffe\\database\\user.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT userid, password FROM users WHERE userid=?", (userid,))
                user = cursor.fetchone()
            return user
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    @staticmethod
    def create_user(userid, password):
        try:
            with sqlite3.connect('C:\\Users\\17590\\PycharmProjects\\onnxcaffe\\database\\user.db') as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (userid, password, authentic, auntheninfo, online) VALUES (?, ?, ?, ?, ?)",
                               (userid, password, False, None, False))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    @staticmethod
    def set_user_online(userid, online_status):
        try:
            with sqlite3.connect('C:\\Users\\17590\\PycharmProjects\\onnxcaffe\\database\\user.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET online=? WHERE userid=?", (online_status, userid))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    @staticmethod
    def set_all_users_offline():
        try:
            with sqlite3.connect('C:\\Users\\17590\\PycharmProjects\\onnxcaffe\\database\\user.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET online=? WHERE online=?", (False, True))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    @staticmethod
    def get_online_user():
        try:
            with sqlite3.connect('C:\\Users\\17590\\PycharmProjects\\onnxcaffe\\database\\user.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT userid, authentic FROM users WHERE online=?", (True,))
                user = cursor.fetchone()
            return user
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    @staticmethod
    def get_users_by_page(page_num, page_size):
        try:
            offset = (page_num - 1) * page_size
            with sqlite3.connect('C:\\Users\\17590\\PycharmProjects\\onnxcaffe\\database\\user.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT userid, password, authentic, auntheninfo, online FROM users LIMIT ? OFFSET ?", (page_size, offset))
                users = cursor.fetchall()
            return users
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    @staticmethod
    def update_user(userid, field, value):
        try:
            with sqlite3.connect('C:\\Users\\17590\\PycharmProjects\\onnxcaffe\\database\\user.db') as conn:
                cursor = conn.cursor()
                cursor.execute(f"UPDATE users SET {field}=? WHERE userid=?", (value, userid))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")


class EnvironmentModel:
    @staticmethod
    def get_data_by_page(page_num, page_size):
        try:
            offset = (page_num - 1) * page_size
            with sqlite3.connect('C:\\Users\\17590\\PycharmProjects\\onnxcaffe\\database\\analyse.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT time, temperature, lighting, Doorswitch, Windowswitch FROM analyse LIMIT ? OFFSET ?", (page_size, offset))
                data = cursor.fetchall()
            return data
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    @staticmethod
    def update_data(time, field, value):
        try:
            with sqlite3.connect('C:\\Users\\17590\\PycharmProjects\\onnxcaffe\\database\\analyse.db') as conn:
                cursor = conn.cursor()
                cursor.execute(f"UPDATE analyse SET {field} = ? WHERE time = ?", (value, time))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
