from app import mysql
from flask_mail import Message
from app import mail
# from app.models.login_m import *

class doctor():
# ADD PATIENT INFORMATION
    def add(self, current_user):
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
    
# ADD MEDICAL CLEARANCE 
    @classmethod
    def add_medical_clearance(cls, patientID, subjectClearance, reason, recommendations, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, oxygenSaturation, painSection, physicalExam, clearance):
        cursor = mysql.connection.cursor()

        sql = "INSERT INTO clearance (patientID, subjectClearance, reason, recommendations, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, oxygenSaturation, painSection, physicalExam, clearance) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (patientID, subjectClearance, reason, recommendations, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, oxygenSaturation, painSection, physicalExam, clearance))
        mysql.connection.commit()

        return True
    
# ADD MEDICAL CERTIFICATE 
    @classmethod
    def add_medical_certificate(cls, patientID, subjectCertificate, reason, recommendations, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, oxygenSaturation, painSection, physicalExam, certificate):
        cursor = mysql.connection.cursor()

        sql = "INSERT INTO certificate (patientID, subjectCertificate, reason, recommendations, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, oxygenSaturation, painSection, physicalExam, certificate) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (patientID, subjectCertificate, reason, recommendations, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, oxygenSaturation, painSection, physicalExam, certificate))
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
    def get_clearances(patientID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM clearance WHERE patientID = %s ORDER BY consultationDate DESC"
        cursor.execute(query, (patientID,))
        clearances = cursor.fetchall()
        cursor.close()
        return clearances
    
    @staticmethod
    def get_certificates(patientID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM certificate WHERE patientID = %s ORDER BY consultationDate DESC"
        cursor.execute(query, (patientID,))
        certificates = cursor.fetchall()
        cursor.close()
        return certificates
    
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
    def get_patient_clearance(patientID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM clearance WHERE patientID = %s"
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
    def get_clearance_info(clearanceID, patientID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM clearance WHERE clearanceID = %s AND patientID = %s"
        cursor.execute(query, (clearanceID, patientID))
        clearance_info  = cursor.fetchone()
        return clearance_info 
    
    @staticmethod
    def get_certificate_info(certificateID, patientID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM certificate WHERE certificateID = %s AND patientID = %s"
        cursor.execute(query, (certificateID, patientID))
        certificate_info  = cursor.fetchone()
        return certificate_info 
    
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
    def update_patient_info(cls, patientID, firstName, midName, lastName, age, civilStatus, gender, bloodType, birthPlace, birthDate, p_address, nationality, religion, eContactName, relationship, eContactNum, occupation, p_email, p_contactNum):
        cursor = mysql.connection.cursor()

        sql = "UPDATE patientinfo SET firstName = %s, midName = %s, lastName = %s, age = %s, civilStatus = %s, gender = %s, bloodType = %s, birthPlace = %s, birthDate = %s, p_address = %s, nationality = %s, religion = %s, eContactName = %s, \
            relationship = %s, eContactNum = %s, occupation = %s, p_email = %s, p_contactNum = %s WHERE patientID = %s"
        cursor.execute(sql, (firstName, midName, lastName, age, civilStatus, gender, bloodType, birthPlace, birthDate, p_address, nationality, religion, eContactName, relationship, eContactNum, occupation, p_email, p_contactNum, patientID))
        print(firstName, midName, lastName, age, civilStatus, gender, bloodType, birthPlace, birthDate, p_address, nationality, religion, eContactName, relationship, eContactNum, occupation, p_email, p_contactNum, patientID)
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
    
# UPDATE PATIENT MEDICAL CLEARANCE
    @classmethod 
    def update_medical_clearance(cls, clearanceID, patientID, subjectClearance, reason, recommendations, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, oxygenSaturation, painSection, physicalExam, clearance):
        cursor = mysql.connection.cursor()

        sql = "UPDATE clearance SET patientID = %s, subjectClearance = %s, reason = %s, recommendations = %s, bloodPressure = %s, pulseRate = %s, temperature = %s, respRate = %s, height = %s, weight_p = %s, bmi = %s, \
            oxygenSaturation = %s, painSection = %s, physicalExam = %s, clearance = %s WHERE clearanceID = %s"
        cursor.execute(sql, (patientID, subjectClearance, reason, recommendations, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, oxygenSaturation, painSection, physicalExam, clearance, clearanceID))
        mysql.connection.commit()

        return True
    
# UPDATE PATIENT MEDICAL CERTIFICATE
    @classmethod 
    def update_medical_certificate(cls, certificateID, patientID, subjectCertificate, reason, recommendations, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, oxygenSaturation, painSection, physicalExam, certificate):
        cursor = mysql.connection.cursor()

        sql = "UPDATE certificate SET patientID = %s, subjectCertificate = %s, reason = %s, recommendations = %s, bloodPressure = %s, pulseRate = %s, temperature = %s, respRate = %s, height = %s, weight_p = %s, bmi = %s, \
            oxygenSaturation = %s, painSection = %s, physicalExam = %s, certificate = %s WHERE certificateID = %s"
        cursor.execute(sql, (patientID, subjectCertificate, reason, recommendations, bloodPressure, pulseRate, temperature, respRate, height, weight_p, bmi, oxygenSaturation, painSection, physicalExam, certificate, certificateID))
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

# DELETE MEDICAL ASSESSMENT
    @classmethod 
    def delete_medical_assessment(cls, assessmentID, patientID):
        cursor = mysql.connection.cursor()
        try:
            query = "DELETE FROM assessment WHERE assessmentID = %s AND patientID = %s"
            cursor.execute(query, (assessmentID, patientID,))
            mysql.connection.commit()
            return True
        except:
            return False

# APPOINTMENT CLASS AND METHODS
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
            return True
        except Exception as e:
            print(f"Error adding appointment: {e}")
            return False
   
    def add_notify(email, reference_number, date_appointment, time_appointment, status_, last_name):
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
    def all(cls, receptionistID):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT appointment.reference_number, appointment.date_appointment, appointment.time_appointment, appointment.last_name, appointment.status_, appointment.doctorName FROM appointment WHERE doctorID = %s ORDER BY date_appointment DESC, TIME(STR_TO_DATE(time_appointment, '%h:%i %p')) DESC"
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
                cls.update_message(
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

    @staticmethod
    def update_message(email, reference_number, date_appointment, time_appointment, status_, last_name):
        print("Sending email to:", email)
        message = Message(
            subject='Appointment Update Information',
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
    def search_appointment(cls, query, doctorID):
        try:
            with mysql.connection.cursor(dictionary=True) as cursor:
                sql = """
                    SELECT appointment.reference_number, appointment.date_appointment, appointment.time_appointment, appointment.last_name, appointment.status_, appointment.doctorName
                    FROM appointment
                    WHERE (LOWER(appointment.reference_number) = %s
                        OR LOWER(appointment.date_appointment) = %s
                        OR LOWER(appointment.time_appointment) = %s
                        OR LOWER(appointment.last_name) = %s
                        OR LOWER(appointment.status_) = %s
                        OR LOWER(appointment.doctorName) = %s)
                        AND appointment.doctorID = %s
                    ORDER BY date_appointment DESC, TIME(STR_TO_DATE(time_appointment, '%h:%i %p')) DESC
                """
                cursor.execute(sql, (query.lower(), query.lower(), query.lower(), query.lower(), query.lower(), query.lower(), doctorID))

                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []

    @classmethod
    def filter_appointment(cls, filter_by, query, doctorID):
        try:
            with mysql.connection.cursor(dictionary=True) as cursor:
                columns = ["all", "reference_number", "date_appointment", "time_appointment", "last_name", "status_", "doctorName"]
                if filter_by not in columns:
                    raise ValueError("Invalid filter column")
                
                elif filter_by == "all":
                    sql = """
                        SELECT appointment.reference_number, appointment.date_appointment, appointment.time_appointment, appointment.last_name, appointment.status_, appointment.doctorName
                        FROM appointment
                        WHERE appointment.doctorID = %s
                        ORDER BY date_appointment DESC, TIME(STR_TO_DATE(time_appointment, '%h:%i %p')) DESC
                    """
                elif filter_by == "reference_number":
                    sql = """
                        SELECT appointment.reference_number, appointment.date_appointment, appointment.time_appointment, appointment.last_name, appointment.status_, appointment.doctorName
                        FROM appointment
                        WHERE LOWER(appointment.reference_number) = %s
                            AND appointment.doctorID = %s
                        ORDER BY date_appointment DESC, TIME(STR_TO_DATE(time_appointment, '%h:%i %p')) DESC
                    """
                else:
                    sql = f"""
                        SELECT appointment.reference_number, appointment.date_appointment, appointment.time_appointment, appointment.last_name, appointment.status_, appointment.doctorName
                        FROM appointment
                        WHERE LOWER(appointment.{filter_by}) = %s
                            AND appointment.doctorID = %s
                        ORDER BY date_appointment DESC, TIME(STR_TO_DATE(time_appointment, '%h:%i %p')) DESC
                    """
                cursor.execute(sql, (query.lower(), doctorID))
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
    def get_all_doctor_name(cls, id):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            sql = "SELECT last_name FROM users WHERE id = %s and user_role = 'doctor'"
            cursor.execute(sql, (id,))
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

    @classmethod
    def get_receptionist_id(cls):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            sql = "SELECT id FROM users WHERE user_role = 'receptionist'"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"Error fetching receptionistID: {e}")
            return []
    @classmethod
    def show_schedule_for_today(cls, doctorID):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            sql = """
                SELECT 
                    date_appointment, 
                    time_appointment, 
                    first_name, 
                    middle_name, 
                    last_name, 
                    status_, 
                    contact_number 
                FROM 
                    appointment 
                WHERE 
                    doctorID = %s 
                    AND (status_ = 'PENDING' or status_ = 'SCHEDULED')
                    AND DATE(date_appointment) = CURDATE()
            """
            cursor.execute(sql, (doctorID,))
            result = cursor.fetchall()
            return result

        except Exception as e:
            print(f"Error showing scheduled for today: {e}")
            return []

class Schedule():
    def __init__(self, date_appointment=None, time_appointment=None, slots=None, doctorID=None, doctorName=None, receptionistID=None):
        self.date_appointment = date_appointment
        self.time_appointment = time_appointment
        self.slots = slots
        self.doctorID = doctorID
        self.doctorName = doctorName
        self.receptionistID = receptionistID
        
    def add_schedule(self):
        try:
            cursor = mysql.connection.cursor()

            check_duplicate_sql = "SELECT date_appointment, time_appointment FROM schedule WHERE date_appointment = %s AND time_appointment = %s"
            cursor.execute(check_duplicate_sql, (self.date_appointment, self.time_appointment))
            existing_schedule = cursor.fetchone()

            if existing_schedule:
                return False
            
            sql = "INSERT INTO schedule(date_appointment, time_appointment, slots, doctorID, doctorName, receptionistID) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (self.date_appointment, self.time_appointment, self.slots, self.doctorID, self.doctorName, self.receptionistID))
            mysql.connection.commit()

            return True
        except Exception as e:
            print(f"Error adding a schedule: {e}")
            print('Data from the user: ', self.date_appointment, self.time_appointment, self.slots, self.doctorID, self.doctorName, self.receptionistID)
            return False
    
    @classmethod
    def all_doctor_schedules(cls, receptionistID):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT schedule.scheduleID, schedule.date_appointment, schedule.time_appointment, schedule.slots, schedule.doctorName FROM schedule WHERE doctorID = %s ORDER BY date_appointment DESC, TIME(STR_TO_DATE(time_appointment, '%h:%i %p')) DESC"
            cursor.execute(sql, (receptionistID,))
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error fetching all appointments: {e}")
            return []

        
    @classmethod
    def delete_schedules(cls, doctorName):
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM schedule WHERE doctorName = %s"
            cursor.execute(sql, (doctorName,))
            mysql.connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting schedule: {e}")
            return False

    @classmethod
    def view_schedule_by_scheduleID(cls, scheduleID):
        cursor = mysql.connection.cursor(dictionary=True)
        query = (
            "SELECT "
            "schedule.scheduleID, schedule.date_appointment, schedule.time_appointment, schedule.slots, "
            "users.first_name AS user_first_name, "
            "users.middle_name AS user_middle_name, "
            "users.last_name AS user_last_name "
            "FROM schedule JOIN users ON schedule.doctorID = users.ID "
            "WHERE schedule.scheduleID = %s"
        )
        cursor.execute(query, (scheduleID,))
        schedule_data = cursor.fetchone()
        print("Schedule Data:", schedule_data)
        cursor.close()
        return schedule_data
    
    @classmethod
    def update_schedule(cls, scheduleID, new_date_appointment, new_time_appointment, new_slots):
        try:
            cursor = mysql.connection.cursor()
            sql = "UPDATE schedule SET date_appointment = %s, time_appointment = %s, slots = %s WHERE scheduleID = %s"
            cursor.execute(sql, (new_date_appointment, new_time_appointment, new_slots, scheduleID))
            mysql.connection.commit()
            
            return True
        except Exception as e:
            print(f"Error updating appointment: {e}")
            return False
    
    @classmethod
    def get_schedule_by_schedule_id(cls, schedule_id):
        print("Reference Number:", schedule_id)
        cursor = mysql.connection.cursor(dictionary=True)  # Set dictionary=True to return results as dictionaries
        cursor.execute("SELECT schedule.scheduleID, schedule.date_appointment, schedule.time_appointment, schedule.slots, schedule.doctorName FROM schedule WHERE scheduleID = %s", (schedule_id,))
        schedule_data = cursor.fetchone()
        print("Schedule Data:", schedule_data)
        cursor.close()
        return schedule_data
    
    @classmethod
    def get_receptionist_ids(cls):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            sql = "SELECT id FROM users WHERE user_role = 'receptionist'"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error fetching doctor ID: {e}")
            return []