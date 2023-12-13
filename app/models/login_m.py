from app import mysql
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, user_id, username, role):
        self.id = user_id
        self.username = username
        self.role = role

    @staticmethod
    def authenticate(username, password):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id, username, password, user_role FROM users WHERE username = %s', (username,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            hash_password = user_data[2] 
            if check_password_hash(hash_password, password): 
                user = User(user_data[0], user_data[1], user_data[3])
                return user
        return None

    @staticmethod
    def get(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id, username, user_role FROM users WHERE id = %s', (user_id,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            user = User(user_data[0], user_data[1], user_data[2])
            return user
        return None