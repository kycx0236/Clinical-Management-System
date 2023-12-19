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
            else:
                # Generate a new hashed password and update the user's password in the database
                new_hashed_password = generate_password_hash(password)
                print("New hashed password", new_hashed_password)
                print("Length of new_hashed_password:", len(new_hashed_password))
                cursor = mysql.connection.cursor()
                update_query = 'UPDATE users SET password = %s WHERE username = %s'
                cursor.execute(update_query, (new_hashed_password, username))
                mysql.connection.commit()
                cursor.close()
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
    
    @staticmethod
    def record_login(user_role, username):
        cursor = mysql.connection.cursor()
        sql_record = """
            INSERT INTO user_logs (log_date, log_time, role, username, action, details) VALUES  
            (CURDATE(), CURTIME(), %s , %s, 'LOGIN', '~~~~~~~~~~~~~~~')
            """
        cursor.execute(sql_record, (user_role, username))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def record_logout(user_role, username):
        cursor = mysql.connection.cursor()
        sql_record = """
            INSERT INTO user_logs (log_date, log_time, role, username, action, details) VALUES  
            (CURDATE(), CURTIME(), %s , %s, 'LOGOUT', '~~~~~~~~~~~~~~~')
            """
        cursor.execute(sql_record, (user_role, username))
        mysql.connection.commit()
        cursor.close()
