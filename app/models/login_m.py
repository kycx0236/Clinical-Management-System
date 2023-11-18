from app import mysql
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id, username, role):
        self.id = user_id
        self.username = username
        self.role = role

    @staticmethod
    def authenticate(username, password):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id, username, user_role FROM users WHERE username = %s AND password = %s', (username, password))
        user_data = cursor.fetchone()
        cursor.close()
      
        if user_data:
            user = User(user_data[0], user_data[1], user_data[2])
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