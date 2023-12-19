class notification():
    
    @classmethod
    def send_notification(cls, notification_type, message_data):
        from app import mysql, socketio
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO notification (notifier, notifying, patientName, notif_type, status, is_read) 
                    VALUES (%s, %s, %s, %s, %s, %s)''', message_data)
        mysql.connection.commit()
        cursor.close()

        socketio.emit('notification', {'type': notification_type, 'message': message_data})
    
    @staticmethod
    def fetch_notifications(notifying_value, notif_type_value):
        from app import mysql
        cursor = mysql.connection.cursor(dictionary=True)
        query = """SELECT notifier, notifying, patientName, notif_type, status, is_read FROM notification WHERE notifying = %s AND notif_type = %s;"""
        cursor.execute(query, (notifying_value, notif_type_value))
        notifications = cursor.fetchall()
        cursor.close()
        return notifications
    
    # @staticmethod
    # def fetch_notifications():
    #     from app import mysql
    #     cursor = mysql.connection.cursor(dictionary=True)
    #     cursor.execute("SELECT * FROM notification")
    #     notifications = cursor.fetchall()
    #     cursor.close()
    #     return notifications
    
    # @staticmethod
    # def fetch_notifications_by_type(notifying, notif_type):
    #     from app import mysql
    #     cursor = mysql.connection.cursor()
    #     query = "SELECT * FROM notification WHERE notifying = %s AND notif_type = %s"
    #     cursor.execute(query, (notifying, notif_type))
    #     notifications = cursor.fetchall()
    #     print('notifications:', notifications)
    #     cursor.close()
    #     return notifications

    # def update_read_notification(notifID):
    #     cursor = mysql.connection.cursor(dictionary=True)
    #     sql = "UPDATE notification SET is_read = True WHERE notifID = %s"
    #     cursor.execute(sql, (notifID,))
    #     mysql.connection.commit()

    #     sql = "SELECT notif_type, notifier FROM notification WHERE id = %s"
    #     cursor.execute(sql, (notifID,))
    #     post_id = cursor.fetchone()
    #     cursor.close()
    #     return post_id
