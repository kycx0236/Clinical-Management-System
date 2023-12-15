from app import mysql
from flask_mail import Message
from app import mail
class Appointment:
    def __init__(self, reference_number=None, receptionistID=None, doctorID=None, doctorName=None, date_appointment=None, time_appointment=None, status_=None, book_date=None, first_name=None, middle_name=None, last_name=None, sex=None, birth_date=None, contact_number=None, email=None, address=None):
        self.reference_number = reference_number
        self.receptionistID = receptionistID
        self.doctorID = doctorID
        self.doctorName = doctorName
        self.date_appointment = date_appointment
        self.time_appointment = time_appointment
        self.status_ = status_
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.sex = sex
        self.birth_date = birth_date
        self.contact_number = contact_number
        self.email = email
        self.address = address

    def add(self):
        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO appointment (reference_number, receptionistID, doctorID, doctorName, date_appointment, time_appointment, status_, first_name, middle_name, last_name, sex, birth_date, contact_number, email, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (self.reference_number, self.receptionistID, self.doctorID, self.doctorName, self.date_appointment, self.time_appointment, self.status_, self.first_name, self.middle_name, self.last_name, self.sex, self.birth_date, self.contact_number, self.email, self.address))
            mysql.connection.commit()
            print("SQL Query:", sql)
            print("Parameters:", (self.reference_number, self.receptionistID, self.doctorID, self.doctorName, self.date_appointment, self.time_appointment, self.status_, self.first_name, self.middle_name, self.last_name, self.sex, self.birth_date, self.contact_number, self.email, self.address))
            return True
        except Exception as e:
            print(f"Error adding appointment: {e}")
            print("SQL Query:", sql)
            print("Parameters:", (self.reference_number, self.receptionistID, self.doctorID, self.doctorName, self.date_appointment, self.time_appointment, self.status_, self.first_name, self.middle_name, self.last_name, self.sex, self.birth_date, self.contact_number, self.email, self.address))
            return False

    @classmethod
    def all(cls, receptionistID):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT appointment.reference_number, appointment.date_appointment, appointment.time_appointment, appointment.last_name, appointment.status_, appointment.doctorName FROM appointment WHERE receptionistID = %s ORDER BY date_appointment DESC, TIME(STR_TO_DATE(time_appointment, '%h:%i %p')) DESC"
            cursor.execute(sql, (receptionistID,))
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error fetching all appointments: {e}")
            return []


    @classmethod
    def delete(cls, reference_number):
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM appointment WHERE reference_number = %s"
            cursor.execute(sql, (reference_number,))
            mysql.connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting appointment: {e}")
            return False

    @classmethod
    def update(cls, reference_number, new_date_appointment, new_time_appointment, new_status_, new_first_name, new_middle_name, new_last_name, new_sex, new_birth_date, new_contact_number, new_email, new_address):
        try:
            cursor = mysql.connection.cursor()
            sql = "UPDATE appointment SET date_appointment = %s, time_appointment = %s, status_ = %s, first_name = %s, middle_name = %s, last_name = %s, sex = %s, birth_date = %s, contact_number = %s, email = %s, address = %s WHERE reference_number = %s"
            cursor.execute(sql, (new_date_appointment, new_time_appointment, new_status_, new_first_name, new_middle_name, new_last_name, new_sex, new_birth_date, new_contact_number, new_email, new_address, reference_number))
            mysql.connection.commit()
            print("Birth Date:", new_birth_date)
            return True
        except Exception as e:
            print(f"Error updating appointment: {e}")
            return False
    
    @classmethod
    def update_second_version(cls, reference_number, new_date_appointment, new_time_appointment, new_status_, new_last_name, new_email):
        try:
            cursor = mysql.connection.cursor()
            sql = "UPDATE appointment SET date_appointment = %s, time_appointment = %s, status_ = %s, last_name = %s, email = %s WHERE reference_number = %s"
            cursor.execute(sql, (new_date_appointment, new_time_appointment, new_status_, new_last_name, new_email, reference_number))
            mysql.connection.commit()

            # Fetch the existing appointment details
            existing_appointment = cls.get_appointment_by_reference_version_two(reference_number)
            print('Existing appointment details:', existing_appointment)
            
            # Check if date, time, or status has changed
            if (new_date_appointment or new_time_appointment or new_status_):
                # Send message if any of the conditions are true
                cls.send_message(
                    new_email,
                    reference_number,
                    new_date_appointment,
                    new_time_appointment,
                    new_status_,
                    existing_appointment['last_name']
                )
            else:
                print('There was an error sending...')

            print("Time Appointment:", new_time_appointment)
            return True
        except Exception as e:
            print(f"Error updating appointment: {e}")
            return False


    # Add print statements for debugging
    @staticmethod
    def send_message(email, reference_number, date_appointment, time_appointment, status_, last_name):
        print("Sending email to:", email)
        message = Message(
            subject='Appointment Information',
            recipients=[email],
            sender=('Receptionist', 'cms_receptionist@gmail.com')
        )
        
        message.html = (
            f"Dear {last_name},<br>"
            f"Your appointment details have been updated:<br>"
            f"Reference Number: {reference_number}<br>"
            f"Date: {date_appointment}<br>"
            f"Time: {time_appointment}<br>"
            f"Status: {status_}<br>"
            "<p>Additional message or instructions can be added here.</p>"
        )
        mail.send(message)
        print("Email sent successfully.")
        
    @classmethod
    def unique_code(cls, reference_number):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT reference_number FROM appointment WHERE reference_number = %s", (reference_number,))
        code = cursor.fetchone()  # Use fetchone() to get a single result
        cursor.close()
        return code
    
    @classmethod
    def get_appointment_by_reference(cls, reference_number):
        print("Reference Number:", reference_number)
        cursor = mysql.connection.cursor(dictionary=True)  # Set dictionary=True to return results as dictionaries
        cursor.execute("SELECT * FROM appointment WHERE reference_number = %s", (reference_number,))
        appointment_data = cursor.fetchone()
        print("Appointment Data:", appointment_data)
        cursor.close()
        return appointment_data
    
    @classmethod
    def get_appointment_by_reference_version_two(cls, reference_number):
        print("Reference Number:", reference_number)
        cursor = mysql.connection.cursor(dictionary=True)  # Set dictionary=True to return results as dictionaries
        cursor.execute("SELECT appointment.reference_number, appointment.date_appointment, appointment.time_appointment, appointment.status_, appointment.last_name, appointment.email, appointment.doctorName FROM appointment WHERE reference_number = %s", (reference_number,))
        appointment_data = cursor.fetchone()
        print("Appointment Data:", appointment_data)
        cursor.close()
        return appointment_data
    
    @classmethod
    def get_booking_reference_details(cls, reference_number):
        cursor = mysql.connection.cursor(dictionary=True) 
        cursor.execute("SELECT last_name, date_appointment, time_appointment, reference_number FROM appointment WHERE reference_number = %s", (reference_number,))
        booking_details = cursor.fetchone()
        cursor.close()
        return booking_details
    
    @classmethod
    def view_appointment_by_reference(cls, reference_number):
        print("Reference Number:", reference_number)
        cursor = mysql.connection.cursor(dictionary=True)
        query = (
            "SELECT "
            "appointment.reference_number, appointment.date_appointment, appointment.time_appointment, "
            "appointment.status_, appointment.book_date, "
            "appointment.first_name AS appointment_first_name, "
            "appointment.middle_name AS appointment_middle_name, "
            "appointment.last_name AS appointment_last_name, "
            "appointment.sex, appointment.birth_date, appointment.contact_number, "
            "appointment.email, appointment.address, "
            "users.first_name AS user_first_name, "
            "users.middle_name AS user_middle_name, "
            "users.last_name AS user_last_name "
            "FROM appointment JOIN users ON appointment.doctorID = users.ID "
            "WHERE appointment.reference_number = %s"
        )
        cursor.execute(query, (reference_number,))
        appointment_data = cursor.fetchone()
        print("Appointment Data:", appointment_data)
        cursor.close()
        return appointment_data
    
    @classmethod
    def search_appointment(cls, query):
        try:
            with mysql.connection.cursor(dictionary=True) as cursor:
                sql = """
                    SELECT appointment.reference_number, appointment.date_appointment, appointment.time_appointment, appointment.last_name, appointment.status_, appointment.doctorName
                    FROM appointment
                    WHERE LOWER(appointment.reference_number) = %s
                    OR LOWER(appointment.date_appointment) = %s
                    OR LOWER(appointment.time_appointment) = %s
                    OR LOWER(appointment.last_name) = %s
                    OR LOWER(appointment.status_) = %s
                    OR LOWER(appointment.doctorName) = %s
                    ORDER BY date_appointment DESC, TIME(STR_TO_DATE(time_appointment, '%h:%i %p')) DESC
                """
                cursor.execute(sql, (query.lower(), query.lower(), query.lower(), query.lower(), query.lower(), query.lower()))

                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []


    @classmethod
    def filter_appointment(cls, filter_by, query):
        try:
            with mysql.connection.cursor(dictionary=True) as cursor:
                columns = ["all", "reference_number", "date_appointment", "time_appointment", "last_name", "status_", "doctorName"]
                if filter_by not in columns:
                    raise ValueError("Invalid filter column")
                
                elif filter_by == "all":
                    sql = """
                        SELECT appointment.reference_number, appointment.date_appointment, appointment.time_appointment, appointment.last_name, appointment.status_, appointment.doctorName
                        FROM appointment
                        ORDER BY date_appointment DESC, TIME(STR_TO_DATE(time_appointment, '%h:%i %p')) DESC
                    """
                elif filter_by == "reference_number":
                    sql = """
                        SELECT appointment.reference_number, appointment.date_appointment, appointment.time_appointment, appointment.last_name, appointment.status_, appointment.doctorName
                        FROM appointment
                        WHERE LOWER(appointment.reference_number) = %s
                        ORDER BY date_appointment DESC, TIME(STR_TO_DATE(time_appointment, '%h:%i %p')) DESC
                    """
                else:
                    sql = f"""
                        SELECT appointment.reference_number, appointment.date_appointment, appointment.time_appointment, appointment.last_name, appointment.status_, appointment.doctorName
                        FROM appointment
                        WHERE LOWER(appointment.{filter_by}) = %s
                        ORDER BY date_appointment DESC, TIME(STR_TO_DATE(time_appointment, '%h:%i %p')) DESC
                    """
                cursor.execute(sql, (query.lower(),))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @classmethod
    def all_time_schedules(cls, selected_date, selected_doctor):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT time_appointment, slots FROM schedule WHERE date_appointment = %s and doctorName = %s ORDER BY date_appointment ASC, TIME(STR_TO_DATE(time_appointment, '%h:%i %p')) ASC;"
            cursor.execute(sql, (selected_date, selected_doctor))
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error fetching all appointments: {e}")
            return []

                
    @classmethod
    def update_slots(cls, selected_date, selected_time, selected_doctor, increment=True):
        try:
            cursor = mysql.connection.cursor()

            # Determine whether to increment or decrement slots
            operator = "+" if increment else "-"

            # Update slots based on the operation and doctorName
            sql = f"UPDATE schedule SET slots = slots {operator} 1 WHERE date_appointment = %s AND time_appointment = %s AND doctorName = %s"
            print("Data from the update slots", selected_date, selected_time, selected_doctor)
            cursor.execute(sql, (selected_date, selected_time, selected_doctor))
            mysql.connection.commit()

            return True
        except Exception as e:
            print(f"Error updating slots: {e}")
            return False


    
    @classmethod
    def update_time_slots(cls, date, new_date, old_time, new_time, doctor_name):
        try:
            cursor = mysql.connection.cursor()
            print('Update time slots data: ', date, new_date, old_time, new_time, doctor_name)
            # Increment slots for the old time
            sql_increment = "UPDATE schedule SET slots = slots + 1 WHERE date_appointment = %s AND time_appointment = %s AND doctorName = %s"
            cursor.execute(sql_increment, (date, old_time, doctor_name))
            mysql.connection.commit()

            # Decrement slots for the new time
            sql_decrement = "UPDATE schedule SET slots = slots - 1 WHERE date_appointment = %s AND time_appointment = %s AND doctorName = %s"
            cursor.execute(sql_decrement, (new_date, new_time, doctor_name))
            mysql.connection.commit()

            return True
        except Exception as e:
            print(f"Error updating slots: {e}")
            return False
        
    @classmethod
    def get_all_reference_numbers(cls):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT reference_number FROM appointment"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error fetching all reference_numbers: {e}")
            return []
    
    @classmethod
    def get_all_available_schedules(cls, date_appointment):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT time_appointment FROM schedule WHERE date_appointment = %s"
            cursor.execute(sql, (date_appointment,))
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error fetching all time schedules: {e}")
            return []

        
    @classmethod
    def update_to_cancel(cls, reference_number, new_status):
        try:
            cursor = mysql.connection.cursor()
            sql = "UPDATE appointment SET status_ = %s WHERE reference_number = %s"
            cursor.execute(sql, (new_status, reference_number))
            mysql.connection.commit()
            print("Appointment updated to cancelled!")
            return True
        except Exception as e:
            print(f"Error deleting appointment: {e}")
            return False
        
    @classmethod
    def get_all_doctor_names(cls):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            sql = "SELECT last_name FROM users WHERE user_role = 'doctor'"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error fetching all doctor names: {e}")
            return []
    
    @classmethod
    def get_doctor_id(cls, doctorName):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            sql = "SELECT id FROM users WHERE last_name = %s and user_role = 'doctor'"
            cursor.execute(sql, (doctorName,))
            result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"Error fetching doctor ID: {e}")
            return []

