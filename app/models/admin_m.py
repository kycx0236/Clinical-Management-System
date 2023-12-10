from app import mysql
from werkzeug.security import generate_password_hash
import string
import random

class admin():

    def get_users():
        cursor = mysql.connection.cursor()
        get_query = "SELECT * FROM users"
        cursor.execute(get_query)
        users = cursor.fetchall()

        user_list = []
        for user in users:
            user_dict = {
                'id': user[0],
                'username': user[1],
                'password': user[2],
                'first_name': user[3],
                'middle_name': user[4],
                'last_name': user[5],
                'gender': user[6],
                'user_role': user[7]
                
            }
            user_list.append(user_dict)

        cursor.close()

        return user_list

    def add_user(self):
        cursor = mysql.connection.cursor()

        check_duplicate_sql = "SELECT * FROM users WHERE username = %s"
        cursor.execute(check_duplicate_sql, (self.username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return False
        
        hashed_password = generate_password_hash(self.password)
        
        sql = "INSERT INTO users (username, password, first_name, middle_name, last_name, gender, user_role) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (self.username, hashed_password, self.first_name, self.middle_name, self.last_name, self.gender, self.user_role))
        mysql.connection.commit()

        return True
    
    def generate_password(length=12):
        special_characters = "!@#$%^&*-_+<>?"
        characters = string.ascii_letters + string.digits + special_characters
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def delete_user_record(user_id):
        cursor = mysql.connection.cursor()

        delete_query = "DELETE FROM users WHERE id = %s"
        cursor.execute(delete_query, (user_id,))
        mysql.connection.commit()

        return True
    
    @staticmethod
    def get_user_info(user_id):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()

        return user
    
    def update_user(user_id, username, password, first_name, middle_name, last_name, gender, user_role):
        cursor = mysql.connection.cursor()

        sql = "UPDATE users SET username=%s, password=%s, first_name=%s, middle_name=%s, last_name=%s, gender=%s, user_role=%s WHERE id=%s"
        cursor.execute(sql, (username, password, first_name, middle_name, last_name, gender, user_role, user_id))
        mysql.connection.commit()

        cursor.close()

        return True
