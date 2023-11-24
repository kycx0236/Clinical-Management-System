from app import mysql

class receptionist():

    @staticmethod
    def get_user(receptionist_id):
        cursor = mysql.connection.cursor()
        query = "SELECT first_name, user_role FROM users WHERE id = %s"
        cursor.execute(query, (receptionist_id,))
        firstname = cursor.fetchone()
        cursor.close()
        return firstname 