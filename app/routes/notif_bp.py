from flask import Blueprint, render_template, jsonify
from flask_login import current_user, login_required
from app.models.notif_m import *
# from app.models.doctor_m import *


notification_bp = Blueprint("notification_bp", __name__)

# @notification_bp.route('/get_notifications/', methods=['GET'])
# def get_notifications():
#     notifications = notification.fetch_notifications()
#     return jsonify(notifications)

# @notification_bp.route('/fetch_notifications/', methods=['GET'])
# def fetch_notifications(user_id, notif_type):
#     notifications = notification.fetch_notifications_by_type(user_id, notif_type)
#     print('notifications in route:', notifications)
#     return jsonify(notifications=notifications)

# For Appointment Status
def appointment_status_notification(notifier_id, notifying_id, notification_type, patient_data):
    if notification_type == 'Done':
        message = f"Dear Doctor, the appointment for {patient_data['firstName']} {patient_data['lastName']} has been successfully completed."
    elif notification_type == 'Cancelled':
        message = f"Dear Doctor, the appointment for {patient_data['firstName']} {patient_data['lastName']} has been cancelled."
    elif notification_type == 'Pending':
        message = f"Dear Doctor, there is a pending appointment for {patient_data['firstName']} {patient_data['lastName']}."
    elif notification_type == 'Scheduled':
        message = f"Dear Doctor, an appointment has been scheduled for {patient_data['firstName']} {patient_data['lastName']}."
    elif notification_type == 'Rescheduled':
        message = f"Dear Doctor, the appointment for {patient_data['firstName']} {patient_data['lastName']} has been rescheduled."

    notification.send_notification(notification_type, (notifier_id, notifying_id, notification_type, 'pending', 'unread'))

# For New Patient Added
def new_patient_added_notification(notifier_id, notifying_id, patient_data):
    message = f"Dear Doctor, {patient_data['firstName']} {patient_data['lastName']} has been added as your new patient. Please review their details."
    notification.send_notification('New Patient Added', (notifier_id, notifying_id, 'NewPatient', 'pending', 'unread'))

# For Lab Request Notification to MedTech
def lab_request_notification_to_medtech(notifier_id, notifying_id, doctor_data, patient_data):
    message = f"Dear MedTech, a lab request has been sent by Dr. {doctor_data['first_name']} {doctor_data['last_name']} for {patient_data['firstName']} {patient_data['lastName']}. Kindly attend to this request."
    notification.send_notification('Lab Request Notification', (notifier_id, notifying_id, 'Request', 'pending', 'unread'))

# For Lab Report Notification to Doctor
def lab_report_notification_to_doctor(notifier_id, notifying_id, patient_name):
    from app import socketio
    message = f"Dear Doctor, the lab report for has been successfully sent. Please review at your earliest convenience."
    notification.send_notification('Lab Report Notification', (notifier_id, notifying_id, patient_name, 'Report', 'pending', 'unread'))
    socketio.emit('lab_report_notification', message, namespace='/')

    notifications = notification.fetch_notifications(notifying_id, 'Report')  
    socketio.emit('notifications_data', {'notifications': notifications})