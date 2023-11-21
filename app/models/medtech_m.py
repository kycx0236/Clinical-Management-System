from app import mysql

class medtech():
# ADD LABORATORY REPORT
    @classmethod 
    def add_laboratory_report(cls, orderID, processName, testResult, refValue, diagnosisReport):
        cursor = mysql.connection.cursor()

        add_report = "INSERT INTO labreport (orderID) VALUES (%s)"
        cursor.execute(add_report, (orderID,))
        reportID = cursor.lastrowid  

        add_test = "INSERT INTO labtest (reportID, processName, testResult, refValue, diagnosisReport) VALUES  (%s, %s, %s, %s, %s)"
        cursor.execute(add_test, (reportID, processName, testResult, refValue, diagnosisReport))
        mysql.connection.commit()
        return True
    
# TO DISPLAY THE LABORATORY REQUESTS IN THE DASHBOARD
    @staticmethod
    def get_lab_requests():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT labrequest.orderID, labrequest.patientID, labrequest.physician, labrequest.patientName FROM labrequest \
                       WHERE NOT EXISTS (SELECT 1 FROM labreport WHERE orderID = labrequest.orderID) ORDER BY labrequest.orderID DESC") 
        labrequest = cursor.fetchall()
        cursor.close()
        return labrequest 
    
    @staticmethod
    def get_lab_reports():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT labrequest.orderID, labrequest.patientID, labrequest.labSubject, labrequest.patientname, labrequest.gender, labrequest.physician, labreport.reportID, labreport.reportDate \
                        FROM labrequest JOIN labreport ON labrequest.orderID = labreport.orderID") 
        labrequest = cursor.fetchall()
        cursor.close()
        return labrequest 
    
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
    def get_lab_report(reportID):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM labtest WHERE reportID = %s"
        cursor.execute(query, (reportID,))
        labreport = cursor.fetchall()
        return labreport
    
# DELETE LABORATORY REPORT
    @classmethod 
    def delete_laboratory_report(cls, reportID, orderID):
        cursor = mysql.connection.cursor()
        try:
            reportQuery = "DELETE FROM labreport WHERE reportID = %s"
            cursor.execute(reportQuery, (reportID,))

            requestQuery = "DELETE FROM labrequest WHERE orderID = %s"
            cursor.execute(requestQuery, (orderID,))

            mysql.connection.commit()
            return True
        except:
            return False