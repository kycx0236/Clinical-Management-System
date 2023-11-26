from app import mysql

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
        
        sql = "INSERT INTO users (username, password, first_name, middle_name, last_name, gender, user_role) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (self.username, self.password, self.first_name, self.middle_name, self.last_name, self.gender, self.user_role))
        mysql.connection.commit()

        return True

    def delete_user_record(user_id):
        cursor = mysql.connection.cursor()

        delete_query = "DELETE FROM users WHERE id = %s"
        cursor.execute(delete_query, (user_id,))
        mysql.connection.commit()

        return True