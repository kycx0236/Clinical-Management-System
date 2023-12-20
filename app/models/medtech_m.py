from app import mysql

class medtech():
# ADD LABORATORY REPORT
    @classmethod 
    def add_laboratory_report(cls,medtech_username, orderID, medtech, pdfFile):
        cursor = mysql.connection.cursor()

        add_report = "INSERT INTO labreport (orderID, medtech, pdfFile) VALUES (%s, %s, %s)"
        cursor.execute(add_report, (orderID, medtech, pdfFile))

        cursor.execute("SELECT patientName FROM labrequest WHERE orderID = %s", (orderID,))
        result = cursor.fetchone()
        patientName = result[0] if result else None

        sql_record = """
        INSERT INTO user_logs (log_date, log_time, role, username, action, details) VALUES  
        (CURDATE(), CURTIME(), 'MEDTECH', %s, 'UPLOAD', CONCAT('Lab Report of ', %s))
        """
        cursor.execute(sql_record, (medtech_username, patientName))

        mysql.connection.commit()
        return True
    
    @staticmethod
    def get_user_info(current_user):
        cursor = mysql.connection.cursor()
        query = ("SELECT first_name, last_name, user_role FROM users WHERE id = %s")
        cursor.execute(query, (current_user,))
        userInfo = cursor.fetchone()
        return userInfo
    
    @staticmethod
    def get_labreport_info(reportID):
        cursor = mysql.connection.cursor()
        query = ("SELECT medtech, pdfFile, reportDate FROM labreport WHERE reportID = %s")
        cursor.execute(query, (reportID,))
        reportInfo = cursor.fetchone()
        return reportInfo

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
                        FROM labrequest JOIN labreport ON labrequest.orderID = labreport.orderID ORDER BY labreport.reportDate DESC") 
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