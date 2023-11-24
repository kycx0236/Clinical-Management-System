from app import mysql

class admin():

    @staticmethod
    def get_user(admin_id):
        cursor = mysql.connection.cursor()
        query = "SELECT first_name, user_role FROM users WHERE id = %s"
        cursor.execute(query, (admin_id,))
        firstname = cursor.fetchone()
        cursor.close()
        return firstname 