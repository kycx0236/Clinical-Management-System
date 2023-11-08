from app import mysql

class doctor():
    
    def add(self):
        cursor = mysql.connection.cursor()

        check_duplicate_sql = "SELECT patientID FROM patientinfo WHERE firstName = %s AND lastName = %s AND birthDate = %s"
        cursor.execute(check_duplicate_sql, (self.firstName, self.lastName, self.birthDate))
        existing_patient = cursor.fetchone()

        if existing_patient:
            return False
        
        sql = "INSERT INTO patientinfo(firstName, midName, lastName, age, civilStatus, gender, bloodType, birthPlace, birthDate, p_address, nationality, religion, eContactName, relationship, eContactNum, occupation, p_email, p_contactNum) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (self.firstName, self.midName, self.lastName, self.age, self.civilStatus, self.gender, self.bloodType, self.birthPlace, self.birthDate, self.p_address, self.nationality, self.religion, self.eContactName, self.relationship, self.eContactNum, self.occupation, self.p_email, self.p_contactNum))

        mysql.connection.commit()

        return True
    
    @classmethod
    def add_medical_history(cls, patientID, bcgCheckbox, dtpCheckbox, pcvCheckbox, influenzaCheckbox, hepaCheckbox, ipvCheckbox, mmrCheckbox, hpvCheckbox, asthmaCheckbox, diabetesCheckbox, heartCheckbox, birthCheckbox, boneCheckbox, alzheimerCheckbox, cancerCheckbox, thyroidCheckbox, tuberculosisCheckbox, eyeCheckbox, clotsCheckbox, mentalCheckbox, kidneyCheckbox, anemiaCheckbox, muscleCheckbox, highbloodCheckbox, epilepsyCheckbox, skinCheckbox, hivCheckbox, pulmonaryCheckbox, specifications, others, past_c1, medication1, dosage1, h_date1, past_c2, medication2, dosage2, h_date2, past_c3, medication3, dosage3, h_date3, habitually, yearsDrunk, frequencyDrink, quitDrinking, frequently, yearsSmoked, frequencySmoke, quitSmoking, often, exerciseType, frequencyExercise, durationActivity, sexActive, sexPartner, numSexPartner, contraception, useDrugs, specifyDrugs, frequencyDrugs, surgeryDate1, surgeryProcedure1, hospital1, surgeryDate2, surgeryProcedure2, hospital2, surgeryDate3, surgeryProcedure3, hospital3, medications, allergies):
        cursor = mysql.connection.cursor()

        sql = "INSERT INTO medicalhistory (patientID, bcgCheckbox, dtpCheckbox, pcvCheckbox, influenzaCheckbox, hepaCheckbox, ipvCheckbox, mmrCheckbox, hpvCheckbox, asthmaCheckbox, diabetesCheckbox, heartCheckbox, birthCheckbox, boneCheckbox, alzheimerCheckbox, cancerCheckbox, thyroidCheckbox, tuberculosisCheckbox, eyeCheckbox, clotsCheckbox, mentalCheckbox, kidneyCheckbox, anemiaCheckbox, muscleCheckbox, highbloodCheckbox, epilepsyCheckbox, skinCheckbox, hivCheckbox, pulmonaryCheckbox, specifications, others, past_c1, medication1, dosage1, h_date1, past_c2, medication2, dosage2, h_date2, past_c3, medication3, dosage3, h_date3, habitually, yearsDrunk, frequencyDrink, quitDrinking, frequently, yearsSmoked, frequencySmoke, quitSmoking, often, exerciseType, frequencyExercise, durationActivity, sexActive, sexPartner, numSexPartner, contraception, useDrugs, specifyDrugs, frequencyDrugs, surgeryDate1, surgeryProcedure1, hospital1, surgeryDate2, surgeryProcedure2, hospital2, surgeryDate3, surgeryProcedure3, hospital3, medications, allergies) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (patientID, bcgCheckbox, dtpCheckbox, pcvCheckbox, influenzaCheckbox, hepaCheckbox, ipvCheckbox, mmrCheckbox, hpvCheckbox, asthmaCheckbox, diabetesCheckbox, heartCheckbox, birthCheckbox, boneCheckbox, alzheimerCheckbox, cancerCheckbox, thyroidCheckbox, tuberculosisCheckbox, eyeCheckbox, clotsCheckbox, mentalCheckbox, kidneyCheckbox, anemiaCheckbox, muscleCheckbox, highbloodCheckbox, epilepsyCheckbox, skinCheckbox, hivCheckbox, pulmonaryCheckbox, specifications, others, past_c1, medication1, dosage1, h_date1, past_c2, medication2, dosage2, h_date2, past_c3, medication3, dosage3, h_date3, habitually, yearsDrunk, frequencyDrink, quitDrinking, frequently, yearsSmoked, frequencySmoke, quitSmoking, often, exerciseType, frequencyExercise, durationActivity, sexActive, sexPartner, numSexPartner, contraception, useDrugs, specifyDrugs, frequencyDrugs, surgeryDate1, surgeryProcedure1, hospital1, surgeryDate2, surgeryProcedure2, hospital2, surgeryDate3, surgeryProcedure3, hospital3, medications, allergies))
        print(patientID, bcgCheckbox, dtpCheckbox, pcvCheckbox, influenzaCheckbox, hepaCheckbox, ipvCheckbox, mmrCheckbox, hpvCheckbox, asthmaCheckbox, diabetesCheckbox, heartCheckbox, birthCheckbox, boneCheckbox, alzheimerCheckbox, cancerCheckbox, thyroidCheckbox, tuberculosisCheckbox, eyeCheckbox, clotsCheckbox, mentalCheckbox, kidneyCheckbox, anemiaCheckbox, muscleCheckbox, highbloodCheckbox, epilepsyCheckbox, skinCheckbox, hivCheckbox, pulmonaryCheckbox, specifications, others, past_c1, medication1, dosage1, h_date1, past_c2, medication2, dosage2, h_date2, past_c3, medication3, dosage3, h_date3, habitually, yearsDrunk, frequencyDrink, quitDrinking, frequently, yearsSmoked, frequencySmoke, quitSmoking, often, exerciseType, frequencyExercise, durationActivity, sexActive, sexPartner, numSexPartner, contraception, useDrugs, specifyDrugs, frequencyDrugs, surgeryDate1, surgeryProcedure1, hospital1, surgeryDate2, surgeryProcedure2, hospital2, surgeryDate3, surgeryProcedure3, hospital3, medications, allergies)
        mysql.connection.commit()

        return True
    
    @classmethod
    def add_medical_assessment(cls, patientID, subjectComp, complaints, illnessHistory, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, normal_head, abnormalities_head, normal_ears, abnormalities_ears, normal_eyes, abnormalities_eyes, normal_nose, abnormalities_nose, normal_skin, abnormalities_skin, normal_back, abnormalities_back, normal_neck, abnormalities_neck, normal_throat, abnormalities_throat, normal_chest, abnormalities_chest, normal_abdomen, abnormalities_abdomen, normal_upper, abnormalities_upper, normal_lower, abnormalities_lower, normal_tract, abnormalities_tract, comments, diagnosis):
        cursor = mysql.connection.cursor()

        sql = "INSERT INTO assessment (patientID, subjectComp, complaints, illnessHistory, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, normal_head, abnormalities_head, normal_ears, abnormalities_ears, normal_eyes, abnormalities_eyes, normal_nose, abnormalities_nose, normal_skin, abnormalities_skin, normal_back, abnormalities_back, normal_neck, abnormalities_neck, normal_throat, abnormalities_throat, normal_chest, abnormalities_chest, normal_abdomen, abnormalities_abdomen, normal_upper, abnormalities_upper, normal_lower, abnormalities_lower, normal_tract, abnormalities_tract, comments, diagnosis) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (patientID, subjectComp, complaints, illnessHistory, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, normal_head, abnormalities_head, normal_ears, abnormalities_ears, normal_eyes, abnormalities_eyes, normal_nose, abnormalities_nose, normal_skin, abnormalities_skin, normal_back, abnormalities_back, normal_neck, abnormalities_neck, normal_throat, abnormalities_throat, normal_chest, abnormalities_chest, normal_abdomen, abnormalities_abdomen, normal_upper, abnormalities_upper, normal_lower, abnormalities_lower, normal_tract, abnormalities_tract, comments, diagnosis))
        print(patientID, subjectComp, complaints, illnessHistory, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, normal_head, abnormalities_head, normal_ears, abnormalities_ears, normal_eyes, abnormalities_eyes, normal_nose, abnormalities_nose, normal_skin, abnormalities_skin, normal_back, abnormalities_back, normal_neck, abnormalities_neck, normal_throat, abnormalities_throat, normal_chest, abnormalities_chest, normal_abdomen, abnormalities_abdomen, normal_upper, abnormalities_upper, normal_lower, abnormalities_lower, normal_tract, abnormalities_tract, comments, diagnosis)
        mysql.connection.commit()

        return True

    @staticmethod
    def get_patients():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM patientinfo") 
        patients = cursor.fetchall()
        cursor.close()
        return patients 
    
    @staticmethod
    def get_consultations(patientID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM assessment WHERE patientID = %s"
        cursor.execute(query, (patientID,))
        consultations = cursor.fetchall()
        cursor.close()
        return consultations
    
    @staticmethod
    def get_patient_info(patientID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM patientinfo WHERE patientID = %s"
        cursor.execute(query, (patientID,))
        patient = cursor.fetchone()
        return patient
    
    @staticmethod
    def get_patient_history(patientID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM medicalhistory WHERE patientID = %s"
        cursor.execute(query, (patientID,))
        patient = cursor.fetchone()
        return patient
    
    @staticmethod
    def get_consultation_info(assessmentID, patientID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM assessment WHERE assessmentID = %s AND patientID = %s"
        cursor.execute(query, (assessmentID, patientID))
        assessment_info  = cursor.fetchone()
        return assessment_info 
    
    @staticmethod
    def get_prescription_info(prescriptionID, assessmentID):
        cursor = mysql.connection.cursor()
        query = """SELECT p.*, pi.firstName, pi.lastName, pi.p_contactNum, pi.p_address, pi.gender, pd.*
                FROM prescription p
                JOIN prescriptiondetails pd ON p.prescriptionID = pd.prescriptionID
                JOIN assessment a ON a.assessmentID = p.assessmentID
                JOIN patientinfo pi ON a.patientID = pi.patientID
                WHERE p.prescriptionID = %s AND a.assessmentID = %s"""
        cursor.execute(query, (prescriptionID, assessmentID))
        prescription_info  = cursor.fetchone()
        return prescription_info 

    @classmethod
    def update_patient_info(cls, patientID, firstName, midName, lastName, age, civilStatus, gender, bloodType, birthPlace, birthDate, p_address, nationality, religion, eContactName, relationship, eContactNum, occupation, p_email, p_contactNum):
        cursor = mysql.connection.cursor()

        sql = "UPDATE patientinfo SET firstName = %s, midName = %s, lastName = %s, age = %s, civilStatus = %s, gender = %s, bloodType = %s, birthPlace = %s, birthDate = %s, p_address = %s, nationality = %s, religion = %s, eContactName = %s, relationship = %s, eContactNum = %s, occupation = %s, p_email = %s, p_contactNum = %s WHERE patientID = %s"
        cursor.execute(sql, (firstName, midName, lastName, age, civilStatus, gender, bloodType, birthPlace, birthDate, p_address, nationality, religion, eContactName, relationship, eContactNum, occupation, p_email, p_contactNum, patientID))
        print(firstName, midName, lastName, age, civilStatus, gender, bloodType, birthPlace, birthDate, p_address, nationality, religion, eContactName, relationship, eContactNum, occupation, p_email, p_contactNum, patientID)
        mysql.connection.commit()
        
        return True

    @classmethod
    def update_medical_history(cls, historyID, patientID, bcgCheckbox, dtpCheckbox, pcvCheckbox, influenzaCheckbox, hepaCheckbox, ipvCheckbox, mmrCheckbox, hpvCheckbox, asthmaCheckbox, diabetesCheckbox, heartCheckbox, birthCheckbox, boneCheckbox, alzheimerCheckbox, cancerCheckbox, thyroidCheckbox, tuberculosisCheckbox, eyeCheckbox, clotsCheckbox, mentalCheckbox, kidneyCheckbox, anemiaCheckbox, muscleCheckbox, highbloodCheckbox, epilepsyCheckbox, skinCheckbox, hivCheckbox, pulmonaryCheckbox, specifications, others, past_c1, medication1, dosage1, h_date1, past_c2, medication2, dosage2, h_date2, past_c3, medication3, dosage3, h_date3, habitually, yearsDrunk, frequencyDrink, quitDrinking, frequently, yearsSmoked, frequencySmoke, quitSmoking, often, exerciseType, frequencyExercise, durationActivity, sexActive, sexPartner, numSexPartner, contraception, useDrugs, specifyDrugs, frequencyDrugs, surgeryDate1, surgeryProcedure1, hospital1, surgeryDate2, surgeryProcedure2, hospital2, surgeryDate3, surgeryProcedure3, hospital3, medications, allergies):
        cursor = mysql.connection.cursor()

        sql = "UPDATE medicalhistory SET patientID = %s, bcgCheckbox = %s, dtpCheckbox = %s, pcvCheckbox = %s, influenzaCheckbox = %s, hepaCheckbox = %s, ipvCheckbox = %s, mmrCheckbox = %s, hpvCheckbox = %s, asthmaCheckbox = %s, diabetesCheckbox = %s, heartCheckbox = %s, birthCheckbox = %s, \
            boneCheckbox = %s, alzheimerCheckbox = %s, cancerCheckbox = %s, thyroidCheckbox = %s, tuberculosisCheckbox = %s, eyeCheckbox = %s, clotsCheckbox = %s, mentalCheckbox = %s, \
            kidneyCheckbox = %s, anemiaCheckbox = %s, muscleCheckbox = %s, highbloodCheckbox = %s, epilepsyCheckbox = %s, skinCheckbox = %s, hivCheckbox = %s, pulmonaryCheckbox = %s, \
            specifications = %s, others = %s, past_c1 = %s, medication1 = %s, dosage1 = %s, h_date1 = %s, past_c2 = %s, medication2 = %s, dosage2 = %s, h_date2 = %s, \
            past_c3 = %s, medication3 = %s, dosage3 = %s, h_date3 = %s, habitually = %s, yearsDrunk = %s, frequencyDrink = %s, quitDrinking = %s,\
            frequently = %s, yearsSmoked = %s, frequencySmoke = %s, quitSmoking = %s, often = %s, exerciseType = %s, frequencyExercise = %s, durationActivity = %s, \
            sexActive = %s, sexPartner = %s, numSexPartner = %s, contraception = %s, useDrugs = %s, specifyDrugs = %s, frequencyDrugs = %s, \
            surgeryDate1 = %s, surgeryProcedure1 = %s, hospital1 = %s, surgeryDate2 = %s, surgeryProcedure2 = %s, hospital2 = %s, \
            surgeryDate3 = %s, surgeryProcedure3 = %s, hospital3 = %s, medications = %s, allergies = %s WHERE historyID = %s"
        cursor.execute(sql, (patientID, bcgCheckbox, dtpCheckbox, pcvCheckbox, influenzaCheckbox, hepaCheckbox, ipvCheckbox, mmrCheckbox, hpvCheckbox, asthmaCheckbox, diabetesCheckbox, heartCheckbox, birthCheckbox, boneCheckbox, alzheimerCheckbox, cancerCheckbox, thyroidCheckbox, tuberculosisCheckbox, eyeCheckbox, clotsCheckbox, mentalCheckbox, kidneyCheckbox, anemiaCheckbox, muscleCheckbox, highbloodCheckbox, epilepsyCheckbox, skinCheckbox, hivCheckbox, pulmonaryCheckbox, specifications, others, past_c1, medication1, dosage1, h_date1, past_c2, medication2, dosage2, h_date2, past_c3, medication3, dosage3, h_date3, habitually, yearsDrunk, frequencyDrink, quitDrinking, frequently, yearsSmoked, frequencySmoke, quitSmoking, often, exerciseType, frequencyExercise, durationActivity, sexActive, sexPartner, numSexPartner, contraception, useDrugs, specifyDrugs, frequencyDrugs, surgeryDate1, surgeryProcedure1, hospital1, surgeryDate2, surgeryProcedure2, hospital2, surgeryDate3, surgeryProcedure3, hospital3, medications, allergies, historyID))
        mysql.connection.commit()
        print('SQL Query:', patientID, bcgCheckbox, dtpCheckbox, pcvCheckbox, influenzaCheckbox, hepaCheckbox, ipvCheckbox, mmrCheckbox, hpvCheckbox, asthmaCheckbox, diabetesCheckbox, heartCheckbox, birthCheckbox, boneCheckbox, alzheimerCheckbox, cancerCheckbox, thyroidCheckbox, tuberculosisCheckbox, eyeCheckbox, clotsCheckbox, mentalCheckbox, kidneyCheckbox, anemiaCheckbox, muscleCheckbox, highbloodCheckbox, epilepsyCheckbox, skinCheckbox, hivCheckbox, pulmonaryCheckbox, specifications, others, past_c1, medication1, dosage1, h_date1, past_c2, medication2, dosage2, h_date2, past_c3, medication3, dosage3, h_date3, habitually, yearsDrunk, frequencyDrink, quitDrinking, frequently, yearsSmoked, frequencySmoke, quitSmoking, often, exerciseType, frequencyExercise, durationActivity, sexActive, sexPartner, numSexPartner, contraception, useDrugs, specifyDrugs, frequencyDrugs, surgeryDate1, surgeryProcedure1, hospital1, surgeryDate2, surgeryProcedure2, hospital2, surgeryDate3, surgeryProcedure3, hospital3, medications, allergies, historyID)

        return True
    
    @classmethod 
    def update_medical_assessment(cls, assessmentID, patientID, subjectComp, complaints, illnessHistory, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, normal_head, abnormalities_head, normal_ears, abnormalities_ears, normal_eyes, abnormalities_eyes, normal_nose, abnormalities_nose, normal_skin, abnormalities_skin, normal_back, abnormalities_back, normal_neck, abnormalities_neck, normal_throat, abnormalities_throat, normal_chest, abnormalities_chest, normal_abdomen, abnormalities_abdomen, normal_upper, abnormalities_upper, normal_lower, abnormalities_lower, normal_tract, abnormalities_tract, comments, diagnosis):
        cursor = mysql.connection.cursor()

        sql = "UPDATE assessment SET patientID = %s, subjectComp = %s, complaints = %s, illnessHistory = %s, bloodPressure = %s, pulseRate = %s, temperature = %s, respRate = %s, height = %s, weight_p = %s, bmi = %s, normal_head = %s, abnormalities_head = %s, normal_ears = %s, abnormalities_ears = %s, normal_eyes = %s, abnormalities_eyes = %s, normal_nose = %s, abnormalities_nose = %s, normal_skin = %s, abnormalities_skin = %s, normal_back = %s, abnormalities_back = %s, normal_neck = %s, abnormalities_neck = %s, normal_throat = %s, abnormalities_throat = %s, normal_chest = %s, abnormalities_chest = %s, normal_abdomen = %s, abnormalities_abdomen = %s, normal_upper = %s, abnormalities_upper = %s, normal_lower = %s, abnormalities_lower = %s, normal_tract = %s, abnormalities_tract = %s, comments = %s, diagnosis = %s WHERE assessmentID = %s"
        cursor.execute(sql, (patientID, subjectComp, complaints, illnessHistory, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, normal_head, abnormalities_head, normal_ears, abnormalities_ears, normal_eyes, abnormalities_eyes, normal_nose, abnormalities_nose, normal_skin, abnormalities_skin, normal_back, abnormalities_back, normal_neck, abnormalities_neck, normal_throat, abnormalities_throat, normal_chest, abnormalities_chest, normal_abdomen, abnormalities_abdomen, normal_upper, abnormalities_upper, normal_lower, abnormalities_lower, normal_tract, abnormalities_tract, comments, diagnosis, assessmentID))
        mysql.connection.commit()
        print('SQL Query:', assessmentID, patientID, subjectComp, complaints, illnessHistory, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, normal_head, abnormalities_head, normal_ears, abnormalities_ears, normal_eyes, abnormalities_eyes, normal_nose, abnormalities_nose, normal_skin, abnormalities_skin, normal_back, abnormalities_back, normal_neck, abnormalities_neck, normal_throat, abnormalities_throat, normal_chest, abnormalities_chest, normal_abdomen, abnormalities_abdomen, normal_upper, abnormalities_upper, normal_lower, abnormalities_lower, normal_tract, abnormalities_tract, comments, diagnosis)

        return True
    
