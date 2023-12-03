from app import mysql
from datetime import date
class Appointment:
    def __init__(self, reference_number=None, date_appointment=None, time_appointment=None, status_=None, book_date=None, first_name=None, middle_name=None, last_name=None, sex=None, birth_date=None, contact_number=None, email=None, address=None):
        self.reference_number = reference_number
        self.date_appointment = date_appointment
        self.time_appointment = time_appointment
        self.status_ = status_
        self.book_date = book_date
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
            sql = "INSERT INTO appointment (reference_number, date_appointment, time_appointment, status_, book_date, first_name, middle_name, last_name, sex, birth_date, contact_number, email, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (self.reference_number, self.date_appointment, self.time_appointment, self.status_, self.book_date, self.first_name, self.middle_name, self.last_name, self.sex, self.birth_date, self.contact_number, self.email, self.address))
            mysql.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding appointment: {e}")
            return False

    @classmethod
    def all(cls):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT * FROM appointment ORDER BY date_appointment DESC, TIME(STR_TO_DATE(time_appointment, '%h:%i %p')) DESC;"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error fetching all appoinments: {e}")
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
        cursor.execute("SELECT * FROM appointment WHERE reference_number = %s", (reference_number,))
        appointment_data = cursor.fetchone()
        print("Appointment Data:", appointment_data)
        cursor.close()
        return appointment_data
    
    @classmethod
    def search_appointment(cls, query):
        try:
            with mysql.connection.cursor() as cursor:
                sql = """
                    SELECT appointment.reference_number, appointment.date_appointment, appointment.time_appointment, appointment.status_
                    FROM appointment
                    WHERE appointment.reference_number = %s
                    OR appointment.date_appointment = %s
                    OR appointment.time_appointment = %s
                    OR appointment.status_ = %s
                """
                cursor.execute(sql, (query, query, query, query))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []


    @classmethod
    def filter_appointment(cls, filter_by, query):
        try:
            with mysql.connection.cursor() as cursor:
                columns = ["reference_number", "date_appointment", "time_appointment", "status_"]
                if filter_by not in columns:
                    raise ValueError("Invalid filter column")

                if filter_by == "reference_number":
                    sql = """
                        SELECT appointment.reference_number, appointment.date_appointment, appointment.time_appointment, appointment.status_
                        FROM appointment
                        WHERE appointment.reference_number = %s
                    """
                else:
                    sql = f"""
                        SELECT appointment.reference_number, appointment.date_appointment, appointment.time_appointment, appointment.status_
                        FROM appointment
                        WHERE appointment.{filter_by} = %s
                    """
                cursor.execute(sql, (query,))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @classmethod
    def all_time_schedules(cls, selected_date):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT time_appointment, slots FROM schedule WHERE date_appointment = %s ORDER BY date_appointment ASC, TIME(STR_TO_DATE(time_appointment, '%h:%i %p')) ASC;"
            cursor.execute(sql, (selected_date,))
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error fetching all appointments: {e}")
            return []

                
    @classmethod
    def update_slots(cls, selected_date, selected_time, increment=True):
        try:
            cursor = mysql.connection.cursor()

            # Determine whether to increment or decrement slots
            operator = "+" if increment else "-"

            # Update slots based on the operation
            sql = f"UPDATE schedule SET slots = slots {operator} 1 WHERE date_appointment = %s AND time_appointment = %s"
            cursor.execute(sql, (selected_date, selected_time))
            mysql.connection.commit()

            return True
        except Exception as e:
            print(f"Error updating slots: {e}")
            return False

    
    @classmethod
    def update_time_slots(cls, date, old_time, new_time):
        try:
            cursor = mysql.connection.cursor()

            # Increment slots for the old time
            sql_increment = "UPDATE schedule SET slots = slots + 1 WHERE date_appointment = %s AND time_appointment = %s"
            cursor.execute(sql_increment, (date, old_time))
            mysql.connection.commit()

            # Decrement slots for the new time
            sql_decrement = "UPDATE schedule SET slots = slots - 1 WHERE date_appointment = %s AND time_appointment = %s"
            cursor.execute(sql_decrement, (date, new_time))
            mysql.connection.commit()

            return True
        except Exception as e:
            print(f"Error updating slots: {e}")
            return False
    
    @classmethod
    def reference_authenticator(cls, reference_number, last_name):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT reference_number FROM appointment WHERE reference_number=%s AND last_name= %s"
            cursor.execute(sql, (reference_number, last_name))
            result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"Error fetching all appointments: {e}")
            return []
        
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
    def get_all_schedule(cls):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT time_appointment FROM schedule"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error fetching all reference_numbers: {e}")
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