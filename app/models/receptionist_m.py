from app import mysql

class receptionist():
# ADD PATIENT INFORMATION
    def add(self):
        cursor = mysql.connection.cursor()

        check_duplicate_sql = "SELECT patientID FROM patientinfo WHERE firstName = %s AND lastName = %s"
        cursor.execute(check_duplicate_sql, (self.firstName, self.lastName))
        existing_patient = cursor.fetchone()

        if existing_patient:
            return False
        
        sql = "INSERT INTO patientinfo(firstName, midName, lastName, age, civilStatus, gender, bloodType, birthPlace, birthDate, p_address, nationality, religion, eContactName, \
            relationship, eContactNum, occupation, p_email, p_contactNum) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (self.firstName, self.midName, self.lastName, self.age, self.civilStatus, self.gender, self.bloodType, self.birthPlace, self.birthDate, 
                             self.p_address, self.nationality, self.religion, self.eContactName, self.relationship, self.eContactNum, self.occupation, self.p_email, 
                             self.p_contactNum))
        mysql.connection.commit()

        return True

# GET USER INFORMATION
    @staticmethod
    def get_user(receptionist_id):
        cursor = mysql.connection.cursor()
        query = "SELECT first_name, user_role FROM users WHERE id = %s"
        cursor.execute(query, (receptionist_id,))
        firstname = cursor.fetchone()

        cursor.close()
        return firstname 

# GET ALL PATIENTS  
    @staticmethod
    def get_patients():
        cursor = mysql.connection.cursor()
        select_doctor_query = "SELECT * FROM patientinfo"
        cursor.execute(select_doctor_query)
        patients = cursor.fetchall()

        cursor.close()
        return patients
    
# GET PATIENT INFORMATION 
    @staticmethod
    def get_patient_info(patientID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM patientinfo WHERE patientID = %s"
        cursor.execute(query, (patientID,))
        patient = cursor.fetchone()
        return patient

# UPDATE PATIENT INFORMATION
    @classmethod
    def update_patient_info(cls, patientID, firstName, midName, lastName, age, civilStatus, gender, bloodType, birthPlace, birthDate, p_address, nationality, religion, eContactName, relationship, eContactNum, occupation, p_email, p_contactNum):
        cursor = mysql.connection.cursor()

        sql = "UPDATE patientinfo SET firstName = %s, midName = %s, lastName = %s, age = %s, civilStatus = %s, gender = %s, bloodType = %s, birthPlace = %s, birthDate = %s, p_address = %s, nationality = %s, religion = %s, eContactName = %s, \
            relationship = %s, eContactNum = %s, occupation = %s, p_email = %s, p_contactNum = %s WHERE patientID = %s"
        cursor.execute(sql, (firstName, midName, lastName, age, civilStatus, gender, bloodType, birthPlace, birthDate, p_address, nationality, religion, eContactName, relationship, eContactNum, occupation, p_email, p_contactNum, patientID))
        print(firstName, midName, lastName, age, civilStatus, gender, bloodType, birthPlace, birthDate, p_address, nationality, religion, eContactName, relationship, eContactNum, occupation, p_email, p_contactNum, patientID)
        mysql.connection.commit()
        
        return True

# DELETE PATIENT RECORD 
    @classmethod 
    def delete_patient_record(cls, patientID):
        cursor = mysql.connection.cursor()
        try:
            query = "DELETE FROM patientinfo WHERE patientID = %s"
            cursor.execute(query, (patientID,))
            mysql.connection.commit()
            return True
        except:
            return False