from app import create_app, mysql
from flask_mail import Message
from app import mail
from app.models.admin_m import admin
from werkzeug.security import generate_password_hash

def seed_data():
    app = create_app()
    with app.app_context():
        conn = mysql._connect()
        cursor = conn.cursor()

        try:
            users_data = [
                {'username': 'admin1', 'first_name': 'admin', 'middle_name': 'admin', 'last_name': 'admin', 'email': 'user1@example.com', 'gender': 'male', 'user_role': 'admin'},

                {'username': 'doctor1', 'first_name': 'doctor', 'middle_name': 'doctor', 'last_name': 'doctor', 'email': 'user2@example.com', 'gender': 'female', 'user_role': 'doctor'},

                {'username': 'medtech1', 'first_name': 'medtech', 'middle_name': 'medtech', 'last_name': 'medtech', 'email': 'user3@example.com', 'gender': 'male', 'user_role': 'medtech'},

                {'username': 'receptionist1', 'first_name': 'receptionist', 'middle_name': 'receptionist', 'last_name': 'receptionist', 'email': 'user4@example.com', 'gender': 'female', 'user_role': 'receptionist'},
            ]

            for user_data in users_data:
                user_data['password'] = admin.generate_password()
                hashed_password = generate_password_hash(user_data['password'])

                query = """INSERT INTO users (username, password, first_name, middle_name, last_name, email, gender, user_role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
                cursor.execute(query, (user_data['username'], hashed_password, user_data['first_name'], user_data['middle_name'], user_data['last_name'], user_data['email'], user_data['gender'], user_data['user_role']))

                admin.send_message(user_data['email'], user_data['password'])

            conn.commit()

            print("Seeding completed successfully.")
        except Exception as e:
            print(f"Error seeding data: {str(e)}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    seed_data()
