from app import mysql
# from app.models.login_m import *

class doctor():
# ADD PATIENT INFORMATION
    def add(self, current_user, doc_username):
        cursor = mysql.connection.cursor()

        check_duplicate_sql = "SELECT patientinfo.patientID FROM patientinfo INNER JOIN docpatient_relation ON patientinfo.patientID = docpatient_relation.patientID \
                            WHERE patientinfo.firstName = %s AND patientinfo.lastName = %s AND docpatient_relation.doctorID = %s"
        cursor.execute(check_duplicate_sql, (self.firstName, self.lastName, current_user))
        existing_patient = cursor.fetchone()

        if existing_patient:
            return False
        
        sql = "INSERT INTO patientinfo(firstName, midName, lastName, age, civilStatus, gender, bloodType, birthPlace, birthDate, p_address, nationality, religion, eContactName, \
            relationship, eContactNum, occupation, p_email, p_contactNum, userID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (self.firstName, self.midName, self.lastName, self.age, self.civilStatus, self.gender, self.bloodType, self.birthPlace, self.birthDate, 
                             self.p_address, self.nationality, self.religion, self.eContactName, self.relationship, self.eContactNum, self.occupation, self.p_email, 
                             self.p_contactNum, self.userID))
        mysql.connection.commit()

        new_patient_id = cursor.lastrowid
        doctor_id = current_user

        sql_docpatient_relation = "INSERT INTO docpatient_relation(doctorID, patientID) VALUES (%s, %s)"
        cursor.execute(sql_docpatient_relation, (doctor_id, new_patient_id))

        sql_record = """
        INSERT INTO user_logs (log_date, log_time, role, username, action, details) VALUES  
        (CURDATE(), CURTIME(), 'DOCTOR', %s, 'ADD', CONCAT('Name: ', %s, ' ', %s))
        """
        cursor.execute(sql_record, (doc_username, self.firstName, self.lastName))

        mysql.connection.commit()

        return True

# ADD PATIENT MEDICAL HISTORY
    @classmethod
    def add_medical_history(cls, patientID, bcgCheckbox, dtpCheckbox, pcvCheckbox, influenzaCheckbox, hepaCheckbox, ipvCheckbox, mmrCheckbox, hpvCheckbox, asthmaCheckbox, diabetesCheckbox, 
                            heartCheckbox, birthCheckbox, boneCheckbox, alzheimerCheckbox, cancerCheckbox, thyroidCheckbox, tuberculosisCheckbox, eyeCheckbox, clotsCheckbox, mentalCheckbox, 
                            kidneyCheckbox, anemiaCheckbox, muscleCheckbox, highbloodCheckbox, epilepsyCheckbox, skinCheckbox, hivCheckbox, pulmonaryCheckbox, specifications, others, past_c1, 
                            medication1, dosage1, h_date1, past_c2, medication2, dosage2, h_date2, past_c3, medication3, dosage3, h_date3, habitually, yearsDrunk, frequencyDrink, quitDrinking, 
                            frequently, yearsSmoked, frequencySmoke, quitSmoking, often, exerciseType, frequencyExercise, durationActivity, sexActive, sexPartner, numSexPartner, contraception, 
                            useDrugs, specifyDrugs, frequencyDrugs, surgeryDate1, surgeryProcedure1, hospital1, surgeryDate2, surgeryProcedure2, hospital2, surgeryDate3, surgeryProcedure3, hospital3, medications, allergies, diet):
        cursor = mysql.connection.cursor()

        sql = "INSERT INTO medicalhistory (patientID, bcgCheckbox, dtpCheckbox, pcvCheckbox, influenzaCheckbox, hepaCheckbox, ipvCheckbox, mmrCheckbox, hpvCheckbox, asthmaCheckbox, diabetesCheckbox, heartCheckbox, birthCheckbox, \
            boneCheckbox, alzheimerCheckbox, cancerCheckbox, thyroidCheckbox, tuberculosisCheckbox, eyeCheckbox, clotsCheckbox, mentalCheckbox, kidneyCheckbox, anemiaCheckbox, muscleCheckbox, highbloodCheckbox, epilepsyCheckbox, \
            skinCheckbox, hivCheckbox, pulmonaryCheckbox, specifications, others, past_c1, medication1, dosage1, h_date1, past_c2, medication2, dosage2, h_date2, past_c3, medication3, dosage3, h_date3, habitually, yearsDrunk, frequencyDrink, \
            quitDrinking, frequently, yearsSmoked, frequencySmoke, quitSmoking, often, exerciseType, frequencyExercise, durationActivity, sexActive, sexPartner, numSexPartner, contraception, useDrugs, specifyDrugs, frequencyDrugs, surgeryDate1, \
            surgeryProcedure1, hospital1, surgeryDate2, surgeryProcedure2, hospital2, surgeryDate3, surgeryProcedure3, hospital3, medications, allergies, diet) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (patientID, bcgCheckbox, dtpCheckbox, pcvCheckbox, influenzaCheckbox, hepaCheckbox, ipvCheckbox, mmrCheckbox, hpvCheckbox, asthmaCheckbox, diabetesCheckbox, heartCheckbox, birthCheckbox, 
                             boneCheckbox, alzheimerCheckbox, cancerCheckbox, thyroidCheckbox, tuberculosisCheckbox, eyeCheckbox, clotsCheckbox, mentalCheckbox, kidneyCheckbox, anemiaCheckbox, muscleCheckbox, highbloodCheckbox, 
                             epilepsyCheckbox, skinCheckbox, hivCheckbox, pulmonaryCheckbox, specifications, others, past_c1, medication1, dosage1, h_date1, past_c2, medication2, dosage2, h_date2, past_c3, medication3, dosage3, 
                             h_date3, habitually, yearsDrunk, frequencyDrink, quitDrinking, frequently, yearsSmoked, frequencySmoke, quitSmoking, often, exerciseType, frequencyExercise, durationActivity, sexActive, sexPartner, 
                             numSexPartner, contraception, useDrugs, specifyDrugs, frequencyDrugs, surgeryDate1, surgeryProcedure1, hospital1, surgeryDate2, surgeryProcedure2, hospital2, surgeryDate3, surgeryProcedure3, hospital3, 
                             medications, allergies, diet))
        mysql.connection.commit()

        return True
    
# ADD PATIENT MEDICAL ASSESSMENT
    @classmethod
    def add_medical_assessment(cls, patientID, subjectComp, complaints, illnessHistory, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, normal_head, abnormalities_head, normal_ears, abnormalities_ears, 
                               normal_eyes, abnormalities_eyes, normal_nose, abnormalities_nose, normal_skin, abnormalities_skin, normal_back, abnormalities_back, normal_neck, abnormalities_neck, normal_throat, abnormalities_throat, 
                               normal_chest, abnormalities_chest, normal_abdomen, abnormalities_abdomen, normal_upper, abnormalities_upper, normal_lower, abnormalities_lower, normal_tract, abnormalities_tract, comments, diagnosis, 
                               oxygenSaturation, painSection):
        cursor = mysql.connection.cursor()

        sql = "INSERT INTO assessment (patientID, subjectComp, complaints, illnessHistory, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, normal_head, abnormalities_head, normal_ears, abnormalities_ears, normal_eyes, \
            abnormalities_eyes, normal_nose, abnormalities_nose, normal_skin, abnormalities_skin, normal_back, abnormalities_back, normal_neck, abnormalities_neck, normal_throat, abnormalities_throat, normal_chest, abnormalities_chest, normal_abdomen, \
            abnormalities_abdomen, normal_upper, abnormalities_upper, normal_lower, abnormalities_lower, normal_tract, abnormalities_tract, comments, diagnosis, oxygenSaturation, painSection) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (patientID, subjectComp, complaints, illnessHistory, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, normal_head, abnormalities_head, normal_ears, abnormalities_ears, normal_eyes, abnormalities_eyes, normal_nose, 
                             abnormalities_nose, normal_skin, abnormalities_skin, normal_back, abnormalities_back, normal_neck, abnormalities_neck, normal_throat, abnormalities_throat, normal_chest, abnormalities_chest, normal_abdomen, abnormalities_abdomen, normal_upper, 
                             abnormalities_upper, normal_lower, abnormalities_lower, normal_tract, abnormalities_tract, comments, diagnosis, oxygenSaturation, painSection))
        mysql.connection.commit()

        return True
    
# ADD PRESCRIPTION
    @classmethod
    def add_prescription(cls, assessment_id, medication_name, dosage, p_quantity, duration, instructions):
        try:
            cursor = mysql.connection.cursor()

            add_prescription = "INSERT INTO prescription (assessmentID) VALUES (%s)"
            cursor.execute(add_prescription, (assessment_id,))
            prescriptionID = cursor.lastrowid  

            add_prescription_details = "INSERT INTO prescriptiondetails (prescriptionID, medication_name, dosage, p_quantity, duration, instructions) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(add_prescription_details, (prescriptionID, medication_name, dosage, p_quantity, duration, instructions))
            mysql.connection.commit()

            return True
        except Exception as e:
            print("Error occurred during prescription addition:", e)
            return False

    @classmethod 
    def add_laboratory_request(cls, patientID, patientName, labSubject, gender, age, physician, orderDate, otherTest, cbcplateCheckbox, hgbhctCheckbox, protimeCheckbox, APTTCheckbox, 
                               bloodtypingCheckbox, ESRCheckbox, plateCheckbox, hgbCheckbox, hctCheckbox, cbcCheckbox, reticsCheckbox, CTBTCheckbox, culsenCheckbox, cultureCheckbox, 
                               gramCheckbox, KOHCheckbox, biopsyCheckbox, papsCheckbox, FNABCheckbox, cellCheckbox, cytolCheckbox, urinCheckbox, stoolCheckbox, occultCheckbox, semenCheckbox, 
                               ELISACheckbox, ASOCheckbox, AntiHBSCheckbox, HCVCheckbox, C3Checkbox, HIVICheckbox, HIVIICheckbox, NS1Checkbox, VDRLCheckbox, PregCheckbox, RFCheckbox, QuantiCheckbox, 
                               QualiCheckbox, TyphidotCheckbox, TubexCheckbox, HAVIgMCheckbox, DengueCheckbox, AFPCheckbox, ferritinCheckbox, HBcIgMCheckbox, AntiHBECheckbox, CA125Checkbox, PROBNPCheckbox, 
                               CA153Checkbox, CA199Checkbox, PSACheckbox, CEACheckbox, FreeT3Checkbox, ANA2Checkbox, FreeT4Checkbox, HBsAGCheckbox, TroponiniCheckbox, HbACheckbox, HBAeAgCheckbox, BetaCheckbox, 
                               T3Checkbox, T4Checkbox, TSHCheckbox, ALPCheckbox, AmylaseCheckbox, BUACheckbox, BUNCheckbox, CreatinineCheckbox, SGPTCheckbox, SGOTCheckbox, FBSCheckbox, RBSCheckbox, HPPCheckbox, 
                               OGCTCheckbox, HGTCheckbox, OGTTCheckbox, NaCheckbox, MgCheckbox, LipidCheckbox, TriglyCheckbox, CholCheckbox, ClCheckbox, TPAGCheckbox, TotalCheckbox, GlobCheckbox, AlbCheckbox, 
                               CKMBCheckbox, CKTotalCheckbox, LDHCheckbox, KCheckbox, CaCheckbox, IonizedCheckbox, PhosCheckbox):
        cursor = mysql.connection.cursor()

        labrequest = "INSERT INTO labrequest (patientID, patientName, labSubject, gender, age, physician, orderDate, otherTest) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(labrequest, (patientID, patientName, labSubject, gender, age, physician, orderDate, otherTest))

        cursor.execute("SELECT LAST_INSERT_ID()")
        orderID = cursor.fetchone()[0]

        hematology = "INSERT INTO hematology (orderID, cbcplateCheckbox, hgbhctCheckbox, protimeCheckbox, APTTCheckbox, bloodtypingCheckbox, ESRCheckbox, plateCheckbox, \
                    hgbCheckbox, hctCheckbox, cbcCheckbox, reticsCheckbox, CTBTCheckbox) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(hematology, (orderID, cbcplateCheckbox, hgbhctCheckbox, protimeCheckbox, APTTCheckbox, bloodtypingCheckbox, ESRCheckbox, plateCheckbox, hgbCheckbox, 
                                    hctCheckbox, cbcCheckbox, reticsCheckbox, CTBTCheckbox))

        bacteriology = "INSERT INTO bacteriology (orderID, culsenCheckbox, cultureCheckbox, gramCheckbox, KOHCheckbox) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(bacteriology, (orderID, culsenCheckbox, cultureCheckbox, gramCheckbox, KOHCheckbox))

        histopathology = "INSERT INTO histopathology (orderID, biopsyCheckbox, papsCheckbox, FNABCheckbox, cellCheckbox, cytolCheckbox) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(histopathology, (orderID, biopsyCheckbox, papsCheckbox, FNABCheckbox, cellCheckbox, cytolCheckbox))

        microscopy = "INSERT INTO microscopy (orderID, urinCheckbox, stoolCheckbox, occultCheckbox, semenCheckbox, ELISACheckbox) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(microscopy, (orderID, urinCheckbox, stoolCheckbox, occultCheckbox, semenCheckbox, ELISACheckbox))

        serology = "INSERT INTO serology (orderID, ASOCheckbox, AntiHBSCheckbox, HCVCheckbox, C3Checkbox, HIVICheckbox, HIVIICheckbox, NS1Checkbox, VDRLCheckbox, PregCheckbox, \
                    RFCheckbox, QuantiCheckbox, QualiCheckbox, TyphidotCheckbox, TubexCheckbox, HAVIgMCheckbox, DengueCheckbox) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(serology, (orderID, ASOCheckbox, AntiHBSCheckbox, HCVCheckbox, C3Checkbox, HIVICheckbox, HIVIICheckbox, NS1Checkbox, VDRLCheckbox, PregCheckbox, RFCheckbox, 
                                  QuantiCheckbox, QualiCheckbox, TyphidotCheckbox, TubexCheckbox, HAVIgMCheckbox, DengueCheckbox))

        immunochem = "INSERT INTO immunochem (orderID, AFPCheckbox, ferritinCheckbox, HBcIgMCheckbox, AntiHBECheckbox, CA125Checkbox, PROBNPCheckbox, CA153Checkbox, CA199Checkbox, \
                    PSACheckbox, CEACheckbox, FreeT3Checkbox, ANA2Checkbox, FreeT4Checkbox, HBsAGCheckbox, TroponiniCheckbox, HbACheckbox, HBAeAgCheckbox, BetaCheckbox, T3Checkbox, \
                    T4Checkbox, TSHCheckbox) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(immunochem, (orderID, AFPCheckbox, ferritinCheckbox, HBcIgMCheckbox, AntiHBECheckbox, CA125Checkbox, PROBNPCheckbox, CA153Checkbox, CA199Checkbox, PSACheckbox, CEACheckbox, 
                                    FreeT3Checkbox, ANA2Checkbox, FreeT4Checkbox, HBsAGCheckbox, TroponiniCheckbox, HbACheckbox, HBAeAgCheckbox, BetaCheckbox, T3Checkbox, T4Checkbox, TSHCheckbox))

        clinicalchem = "INSERT INTO clinicalchem (orderID, ALPCheckbox, AmylaseCheckbox, BUACheckbox, BUNCheckbox, CreatinineCheckbox, SGPTCheckbox, SGOTCheckbox, FBSCheckbox, RBSCheckbox, \
                    HPPCheckbox, OGCTCheckbox, HGTCheckbox, OGTTCheckbox, NaCheckbox, MgCheckbox, LipidCheckbox, TriglyCheckbox, CholCheckbox, ClCheckbox, TPAGCheckbox, TotalCheckbox, GlobCheckbox, \
                    AlbCheckbox, CKMBCheckbox, CKTotalCheckbox, LDHCheckbox, KCheckbox, CaCheckbox, IonizedCheckbox, PhosCheckbox) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(clinicalchem, (orderID, ALPCheckbox, AmylaseCheckbox, BUACheckbox, BUNCheckbox, CreatinineCheckbox, SGPTCheckbox, SGOTCheckbox, FBSCheckbox, RBSCheckbox, HPPCheckbox, OGCTCheckbox, 
                                      HGTCheckbox, OGTTCheckbox, NaCheckbox, MgCheckbox, LipidCheckbox, TriglyCheckbox, CholCheckbox, ClCheckbox, TPAGCheckbox, TotalCheckbox, GlobCheckbox, AlbCheckbox, 
                                      CKMBCheckbox, CKTotalCheckbox, LDHCheckbox, KCheckbox, CaCheckbox, IonizedCheckbox, PhosCheckbox))
        mysql.connection.commit()
        return True
    
# GET INFORMATION
    @staticmethod
    def get_doctor_info(doctor_id):
        cursor = mysql.connection.cursor()
        query = "SELECT first_name, last_name, user_role FROM users WHERE id = %s"
        cursor.execute(query, (doctor_id,))
        doctor = cursor.fetchone()
        cursor.close()
        return doctor

    @staticmethod
    def get_patients(doctorID):
        cursor = mysql.connection.cursor()
        select_doctor_query = "SELECT patientID FROM docpatient_relation WHERE doctorID = %s"
        cursor.execute(select_doctor_query, (doctorID,))
        patient_ids = cursor.fetchall()

        patient_records = []

        for patient_id in patient_ids:
            select_patient_query = "SELECT * FROM patientinfo WHERE patientID = %s"
            cursor.execute(select_patient_query, (patient_id[0],))
            patient_data = cursor.fetchone()
            patient_records.append(patient_data)

        cursor.close()

        return patient_records

    @staticmethod
    def get_consultations(patientID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM assessment WHERE patientID = %s ORDER BY consultationDate DESC"
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
    def get_prescription_info(assessmentID):
        cursor = mysql.connection.cursor()
        query = "SELECT prescriptiondetails.medication_name, prescriptiondetails.dosage, prescriptiondetails.p_quantity, prescriptiondetails.duration, prescriptiondetails.instructions \
                FROM prescription JOIN prescriptiondetails ON prescription.prescriptionID = prescriptiondetails.prescriptionID WHERE prescription.assessmentID = %s"
        cursor.execute(query, (assessmentID,))
        prescription_info  = cursor.fetchall()
        return prescription_info 

    @staticmethod
    def get_labrequest_data(orderID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM labrequest WHERE orderID = %s"
        cursor.execute(query, (orderID,))
        labreqdata = cursor.fetchone()
        return labreqdata
    
    @staticmethod
    def get_hematology_data(orderID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM hematology WHERE orderID = %s"
        cursor.execute(query, (orderID,))
        hematology_data = cursor.fetchone()
        cursor.close()
        return hematology_data

    @staticmethod
    def get_bacteriology_data(orderID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM bacteriology WHERE orderID = %s"
        cursor.execute(query, (orderID,))
        bacteriology_data = cursor.fetchone()
        cursor.close()
        return bacteriology_data
    
    @staticmethod
    def get_histopathology_data(orderID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM histopathology WHERE orderID = %s"
        cursor.execute(query, (orderID,))
        histopathology_data = cursor.fetchone()
        cursor.close()
        return histopathology_data
    
    @staticmethod
    def get_microscopy_data(orderID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM microscopy WHERE orderID = %s"
        cursor.execute(query, (orderID,))
        microscopy_data = cursor.fetchone()
        cursor.close()
        return microscopy_data
    
    @staticmethod
    def get_serology_data(orderID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM serology WHERE orderID = %s"
        cursor.execute(query, (orderID,))
        serology_data = cursor.fetchone()
        cursor.close()
        return serology_data
    
    @staticmethod
    def get_immunochem_data(orderID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM immunochem WHERE orderID = %s"
        cursor.execute(query, (orderID,))
        immunochem_data = cursor.fetchone()
        cursor.close()
        return immunochem_data
    
    @staticmethod
    def get_clinicalchem_data(orderID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM clinicalchem WHERE orderID = %s"
        cursor.execute(query, (orderID,))
        clinicalchem_data = cursor.fetchone()
        cursor.close()
        return clinicalchem_data
    
    @staticmethod
    def get_lab_reports(patientID):
        cursor = mysql.connection.cursor()
        query = "SELECT labrequest.labSubject, labreport.reportDate, labrequest.orderID, labrequest.patientID , labreport.reportID \
                FROM labrequest JOIN labreport ON labrequest.orderID = labreport.orderID \
                WHERE labrequest.patientID = %s"
        cursor.execute(query, (patientID,))
        lab_reports = cursor.fetchall()
        return lab_reports
    
    @staticmethod
    def get_labreport_info(reportID):
        cursor = mysql.connection.cursor()
        query = ("SELECT medtech, pdfFile, reportDate FROM labreport WHERE reportID = %s")
        cursor.execute(query, (reportID,))
        reportInfo = cursor.fetchone()
        return reportInfo

# UPDATE PATIENT INFORMATION
    @classmethod
    def update_patient_info(cls, doc_username, patientID, firstName, midName, lastName, age, civilStatus, gender, bloodType, birthPlace, birthDate, p_address, nationality, religion, eContactName, relationship, eContactNum, occupation, p_email, p_contactNum):
        cursor = mysql.connection.cursor()

        sql = "UPDATE patientinfo SET firstName = %s, midName = %s, lastName = %s, age = %s, civilStatus = %s, gender = %s, bloodType = %s, birthPlace = %s, birthDate = %s, p_address = %s, nationality = %s, religion = %s, eContactName = %s, \
            relationship = %s, eContactNum = %s, occupation = %s, p_email = %s, p_contactNum = %s WHERE patientID = %s"
        cursor.execute(sql, (firstName, midName, lastName, age, civilStatus, gender, bloodType, birthPlace, birthDate, p_address, nationality, religion, eContactName, relationship, eContactNum, occupation, p_email, p_contactNum, patientID))
        print(firstName, midName, lastName, age, civilStatus, gender, bloodType, birthPlace, birthDate, p_address, nationality, religion, eContactName, relationship, eContactNum, occupation, p_email, p_contactNum, patientID)

        sql_record = """
        INSERT INTO user_logs (log_date, log_time, role, username, action, details) VALUES  
        (CURDATE(), CURTIME(), 'DOCTOR', %s, 'EDIT', CONCAT('Name: ', %s, ' ', %s))
        """
        cursor.execute(sql_record, (doc_username, firstName, lastName))

        mysql.connection.commit()
        
        return True

# UPDATE PATIENT MEDICAL HISTORY
    @classmethod
    def update_medical_history(cls, historyID, patientID, bcgCheckbox, dtpCheckbox, pcvCheckbox, influenzaCheckbox, hepaCheckbox, ipvCheckbox, mmrCheckbox, hpvCheckbox, asthmaCheckbox, diabetesCheckbox, heartCheckbox, birthCheckbox, 
                               boneCheckbox, alzheimerCheckbox, cancerCheckbox, thyroidCheckbox, tuberculosisCheckbox, eyeCheckbox, clotsCheckbox, mentalCheckbox, kidneyCheckbox, anemiaCheckbox, muscleCheckbox, highbloodCheckbox, 
                               epilepsyCheckbox, skinCheckbox, hivCheckbox, pulmonaryCheckbox, specifications, others, past_c1, medication1, dosage1, h_date1, past_c2, medication2, dosage2, h_date2, past_c3, medication3, dosage3, 
                               h_date3, habitually, yearsDrunk, frequencyDrink, quitDrinking, frequently, yearsSmoked, frequencySmoke, quitSmoking, often, exerciseType, frequencyExercise, durationActivity, sexActive, sexPartner, 
                               numSexPartner, contraception, useDrugs, specifyDrugs, frequencyDrugs, surgeryDate1, surgeryProcedure1, hospital1, surgeryDate2, surgeryProcedure2, hospital2, surgeryDate3, surgeryProcedure3, hospital3, 
                               medications, allergies, diet):
        cursor = mysql.connection.cursor()

        sql = "UPDATE medicalhistory SET patientID = %s, bcgCheckbox = %s, dtpCheckbox = %s, pcvCheckbox = %s, influenzaCheckbox = %s, hepaCheckbox = %s, ipvCheckbox = %s, mmrCheckbox = %s, hpvCheckbox = %s, asthmaCheckbox = %s, diabetesCheckbox = %s,  \
            heartCheckbox = %s, birthCheckbox = %s, boneCheckbox = %s, alzheimerCheckbox = %s, cancerCheckbox = %s, thyroidCheckbox = %s, tuberculosisCheckbox = %s, eyeCheckbox = %s, clotsCheckbox = %s, mentalCheckbox = %s, \
            kidneyCheckbox = %s, anemiaCheckbox = %s, muscleCheckbox = %s, highbloodCheckbox = %s, epilepsyCheckbox = %s, skinCheckbox = %s, hivCheckbox = %s, pulmonaryCheckbox = %s, \
            specifications = %s, others = %s, past_c1 = %s, medication1 = %s, dosage1 = %s, h_date1 = %s, past_c2 = %s, medication2 = %s, dosage2 = %s, h_date2 = %s, \
            past_c3 = %s, medication3 = %s, dosage3 = %s, h_date3 = %s, habitually = %s, yearsDrunk = %s, frequencyDrink = %s, quitDrinking = %s,\
            frequently = %s, yearsSmoked = %s, frequencySmoke = %s, quitSmoking = %s, often = %s, exerciseType = %s, frequencyExercise = %s, durationActivity = %s, \
            sexActive = %s, sexPartner = %s, numSexPartner = %s, contraception = %s, useDrugs = %s, specifyDrugs = %s, frequencyDrugs = %s, \
            surgeryDate1 = %s, surgeryProcedure1 = %s, hospital1 = %s, surgeryDate2 = %s, surgeryProcedure2 = %s, hospital2 = %s, \
            surgeryDate3 = %s, surgeryProcedure3 = %s, hospital3 = %s, medications = %s, allergies = %s, diet = %s WHERE historyID = %s"
        cursor.execute(sql, (patientID, bcgCheckbox, dtpCheckbox, pcvCheckbox, influenzaCheckbox, hepaCheckbox, ipvCheckbox, mmrCheckbox, hpvCheckbox, asthmaCheckbox, diabetesCheckbox, heartCheckbox, birthCheckbox, boneCheckbox, 
                             alzheimerCheckbox, cancerCheckbox, thyroidCheckbox, tuberculosisCheckbox, eyeCheckbox, clotsCheckbox, mentalCheckbox, kidneyCheckbox, anemiaCheckbox, muscleCheckbox, highbloodCheckbox, epilepsyCheckbox, 
                             skinCheckbox, hivCheckbox, pulmonaryCheckbox, specifications, others, past_c1, medication1, dosage1, h_date1, past_c2, medication2, dosage2, h_date2, past_c3, medication3, dosage3, h_date3, habitually, 
                             yearsDrunk, frequencyDrink, quitDrinking, frequently, yearsSmoked, frequencySmoke, quitSmoking, often, exerciseType, frequencyExercise, durationActivity, sexActive, sexPartner, numSexPartner, contraception, 
                             useDrugs, specifyDrugs, frequencyDrugs, surgeryDate1, surgeryProcedure1, hospital1, surgeryDate2, surgeryProcedure2, hospital2, surgeryDate3, surgeryProcedure3, hospital3, medications, allergies, diet, historyID))
        mysql.connection.commit()

        return True
    
# UPDATE PATIENT MEDICAL ASSESSMENT
    @classmethod 
    def update_medical_assessment(cls, assessmentID, patientID, subjectComp, complaints, illnessHistory, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, normal_head, abnormalities_head, normal_ears, abnormalities_ears, 
                                  normal_eyes, abnormalities_eyes, normal_nose, abnormalities_nose, normal_skin, abnormalities_skin, normal_back, abnormalities_back, normal_neck, abnormalities_neck, normal_throat, abnormalities_throat, normal_chest, 
                                  abnormalities_chest, normal_abdomen, abnormalities_abdomen, normal_upper, abnormalities_upper, normal_lower, abnormalities_lower, normal_tract, abnormalities_tract, comments, diagnosis, oxygenSaturation, painSection):
        cursor = mysql.connection.cursor()

        sql = "UPDATE assessment SET patientID = %s, subjectComp = %s, complaints = %s, illnessHistory = %s, bloodPressure = %s, pulseRate = %s, temperature = %s, respRate = %s, height = %s, weight_p = %s, bmi = %s, normal_head = %s, abnormalities_head = %s, \
            normal_ears = %s, abnormalities_ears = %s, normal_eyes = %s, abnormalities_eyes = %s, normal_nose = %s, abnormalities_nose = %s, normal_skin = %s, abnormalities_skin = %s, normal_back = %s, abnormalities_back = %s, normal_neck = %s, abnormalities_neck = %s, \
            normal_throat = %s, abnormalities_throat = %s, normal_chest = %s, abnormalities_chest = %s, normal_abdomen = %s, abnormalities_abdomen = %s, normal_upper = %s, abnormalities_upper = %s, normal_lower = %s, abnormalities_lower = %s, normal_tract = %s, \
            abnormalities_tract = %s, comments = %s, diagnosis = %s, oxygenSaturation = %s, painSection = %s WHERE assessmentID = %s"
        cursor.execute(sql, (patientID, subjectComp, complaints, illnessHistory, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, normal_head, abnormalities_head, normal_ears, abnormalities_ears, normal_eyes, abnormalities_eyes, 
                             normal_nose, abnormalities_nose, normal_skin, abnormalities_skin, normal_back, abnormalities_back, normal_neck, abnormalities_neck, normal_throat, abnormalities_throat, normal_chest, abnormalities_chest, normal_abdomen, 
                             abnormalities_abdomen, normal_upper, abnormalities_upper, normal_lower, abnormalities_lower, normal_tract, abnormalities_tract, comments, diagnosis, oxygenSaturation, painSection, assessmentID))
        mysql.connection.commit()

        return True
    
# DELETE PATIENT RECORD
    @classmethod 
    def delete_patient_record(cls, patientID, doc_username):
        cursor = mysql.connection.cursor()
        try:
            fetch_name_query = "SELECT firstName, lastName FROM patientinfo WHERE patientID = %s"
            cursor.execute(fetch_name_query, (patientID,))
            name_tuple = cursor.fetchone()
            patient_fname = name_tuple[0]
            patient_lname = name_tuple[1]

            query = "DELETE FROM patientinfo WHERE patientID = %s"
            cursor.execute(query, (patientID,))

            sql_record = """
            INSERT INTO user_logs (log_date, log_time, role, username, action, details) VALUES  
            (CURDATE(), CURTIME(), 'DOCTOR', %s, 'DELETE', CONCAT('Name: ', %s, ' ', %s))
            """
            cursor.execute(sql_record, (doc_username, patient_fname, patient_lname))

            mysql.connection.commit()
            return True
        except:
            return False