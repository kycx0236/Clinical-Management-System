from app import mysql

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
            sql = "INSERT INTO students (id_number, first_name, last_name, course_code, year_, gender) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (self.id_number, self.first_name, self.last_name, self.course_code, self.year_, self.gender))
            mysql.connection.commit()
            return True
        except Exception as e:
            # You might want to log this error for debugging purposes
            print(f"Error adding student: {e}")
            return False

    @classmethod
    def all(cls):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT * FROM appointment"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            # You might want to log this error for debugging purposes
            print(f"Error fetching all students: {e}")
            return []

    @classmethod
    def delete(cls, id_number):
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM students WHERE id_number = %s"
            cursor.execute(sql, (id_number,))
            mysql.connection.commit()
            return True
        except Exception as e:
            # You might want to log this error for debugging purposes
            print(f"Error deleting student: {e}")
            return False

    @classmethod
    def update(cls, id_number, new_first_name, new_last_name, new_course_code, new_year_, new_gender):
        try:
            cursor = mysql.connection.cursor()
            sql = "UPDATE students SET first_name = %s, last_name = %s, course_code = %s, year_ = %s, gender = %s WHERE id_number = %s"
            cursor.execute(sql, (new_first_name, new_last_name, new_course_code, new_year_, new_gender, id_number))
            mysql.connection.commit()
            return True
        except Exception as e:
            # You might want to log this error for debugging purposes
            print(f"Error updating student: {e}")
            return False
        
    @classmethod
    def unique_code(cls, id_number):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id_number FROM students WHERE id_number = %s", (id_number,))
        code = cursor.fetchone()  # Use fetchone() to get a single result
        cursor.close()
        return code
    
    @classmethod
    def get_student_by_id(cls, id_number):
        cursor = mysql.connection.cursor(dictionary=True)  # Set dictionary=True to return results as dictionaries
        cursor.execute("SELECT * FROM students WHERE id_number = %s", (id_number,))
        student_data = cursor.fetchone()
        cursor.close()
        return student_data

    @classmethod
    def search_student(cls, query):
        try:
            with mysql.connection.cursor() as cursor:
                sql = """
                    SELECT students.id_number, students.first_name, students.last_name, students.course_code, courses.college_code, students.year_, students.gender
                    FROM students
                    JOIN courses ON students.course_code = courses.course_code
                    WHERE students.id_number = %s
                    OR students.first_name = %s
                    OR students.last_name = %s
                    OR students.course_code = %s
                    OR courses.college_code = %s
                    OR students.year_ = %s
                    OR students.gender = %s
                """
                cursor.execute(sql, (query, query, query, query, query, query, query))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []

    @classmethod
    def filter_student(cls, filter_by, query):
        try:
            with mysql.connection.cursor() as cursor:
                # Construct the SQL query based on the selected column
                columns = ["id_number", "first_name", "last_name", "course_code", "college_code", "year_", "gender"]
                if filter_by not in columns:
                    raise ValueError("Invalid filter column")
                if filter_by == "college_code":
                    sql = f"""
                        SELECT students.id_number, students.first_name, students.last_name, students.course_code, courses.college_code, students.year_, students.gender
                        FROM students
                        JOIN courses ON students.course_code = courses.course_code
                        WHERE courses.college_code = %s
                    """
                else:
                    sql = f"""
                        SELECT students.id_number, students.first_name, students.last_name, students.course_code, courses.college_code, students.year_, students.gender
                        FROM students
                        JOIN courses ON students.course_code = courses.course_code
                        WHERE students.{filter_by} = %s
                    """
                cursor.execute(sql, (query,))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []
        
    @classmethod
    def get_all_courses(cls):
        try:
            cursor = mysql.connection.cursor(dictionary=True)  # Set dictionary=True to return results as dictionaries
            cursor.execute("SELECT course_code FROM courses")
            all_courses = cursor.fetchall()
            cursor.close()
            return all_courses
        except Exception as e:
            print(f"Error obtaining course_code: {e}")
            return False
        
    @classmethod
    def get_all_colleges(cls, id_number):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT courses.college_code 
                FROM courses
                JOIN students
                ON students.course_code = courses.course_code
                WHERE id_number = %s
            """, (id_number,))
            all_colleges = cursor.fetchall()
            cursor.close()
            return all_colleges
        except Exception as e:
            print(f"Error obtaining college_code: {e}")
            return False
