from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required, logout_user, current_user
from app.routes.utils import role_required
from app.forms.medtech_f import *
from app.models.medtech_m import *
from app.routes.notif_bp import *
import app.models as models
from flask import Blueprint
from cloudinary import uploader
from cloudinary.uploader import upload
from cloudinary.uploader import destroy
from app import socketio 

medtech_bp = Blueprint('medtech', __name__)

# @socketio.on('new_lab_report')
# def handle_new_lab_report():
#     socketio.emit('new_lab_report_notification', {'data': 'New laboratory report added'}, broadcast=True)

# LAB REQUEST TABLE
@medtech_bp.route('/')
@login_required
@role_required('medtech')
def dashboard():
    current_id = current_user.id 
    medtech_info = medtech.get_user_info(current_id)
    labrequest_data = medtech.get_lab_requests()
    labreport_data = medtech.get_lab_reports()
    limited_patient = labreport_data[:5]

    return render_template("medtech/dashboard.html", labrequests=labrequest_data, info=medtech_info, patients=limited_patient)

@medtech_bp.route('/laboratory_test/', methods=['GET', 'POST'])
@login_required
@role_required('medtech')
def laboratory_test():
    form=PatientForm()
    patient_id = None
    user_id = current_user.id
    user_info = medtech.get_user_info(user_id)

    if request.method == 'GET':
        order_id = request.args.get('order_id')
        patient_id = request.args.get('patient_id')
        labreq_info = medtech.get_labrequest_data(order_id)
        hematology_info = medtech.get_hematology_data(order_id)
        bacteriology_info = medtech.get_bacteriology_data(order_id)
        histopathology_info = medtech.get_histopathology_data(order_id)
        microscopy_info = medtech.get_microscopy_data(order_id)
        serology_info = medtech.get_serology_data(order_id)
        immunochem_info = medtech.get_immunochem_data(order_id)
        clinicalchem_info = medtech.get_clinicalchem_data(order_id)
        user_info = medtech.get_user_info(user_id)

        return render_template('medtech/laboratory_test.html', labreq=labreq_info, PatientForm=form, 
                               patient_id=patient_id, hematology=hematology_info, bacteriology=bacteriology_info,
                               histopathology=histopathology_info, microscopy=microscopy_info, serology=serology_info,
                               immunochem=immunochem_info, clinicalchem=clinicalchem_info, medtech=user_info, socketio=socketio)
    
    elif request.method == 'POST':
        new_order_id = request.form.get('order_id')
        new_doctor_id = request.form.get('doctor_id')
        new_medtech_name = request.form.get('medtech_name')
        patientName = request.form.get('fullName')
        uploaded_file = request.files['pdfFile']

        if uploaded_file.filename != '' and uploaded_file.filename.endswith('.pdf'):
           
            uploaded_result = uploader.upload(uploaded_file)
            pdf_url = uploaded_result['url']
            print('pdf_url:', pdf_url)

            report = medtech.add_laboratory_report(orderID=new_order_id, medtech=new_medtech_name, pdfFile=pdf_url)

            labreq_info = medtech.get_labrequest_data(new_order_id)
            hematology_info = medtech.get_hematology_data(new_order_id)
            bacteriology_info = medtech.get_bacteriology_data(new_order_id)
            histopathology_info = medtech.get_histopathology_data(new_order_id)
            microscopy_info = medtech.get_microscopy_data(new_order_id)
            serology_info = medtech.get_serology_data(new_order_id)
            immunochem_info = medtech.get_immunochem_data(new_order_id)
            clinicalchem_info = medtech.get_clinicalchem_data(new_order_id)
            user_info = medtech.get_user_info(user_id)

            if report:
                # socketio.emit('new_lab_report_notification', namespace='/')
                notifier_id = current_user.id 
                notifying_id = new_doctor_id
                patient_name = request.form.get('fullName')
                # print('NOTIFIER ID::', patient_data)
                # print('DOCTOR ID:', notifying_id)
                print('PATIENT:', patient_name)
                
                lab_report_notification_to_doctor(notifier_id, notifying_id, patient_name)
                
                return render_template("medtech/laboratory_test.html", success=True, labreq=labreq_info, PatientForm=form, 
                               patient_id=patient_id, hematology=hematology_info, bacteriology=bacteriology_info,
                               histopathology=histopathology_info, microscopy=microscopy_info, serology=serology_info,
                               immunochem=immunochem_info, clinicalchem=clinicalchem_info, medtech=user_info)
            else:
                return render_template("medtech/laboratory_test.html", error=True, labreq=labreq_info, PatientForm=form, 
                               patient_id=patient_id, hematology=hematology_info, bacteriology=bacteriology_info,
                               histopathology=histopathology_info, microscopy=microscopy_info, serology=serology_info,
                               immunochem=immunochem_info, clinicalchem=clinicalchem_info, medtech=user_info)
        
    return render_template("medtech/laboratory_test.html", patient_id=patient_id, medtech=user_info, socketio=socketio)

@medtech_bp.route('/patient/')
@login_required
@role_required('medtech')
def patient():
    user_id = current_user.id
    labrequest_data = medtech.get_lab_reports()
    medtech_info = medtech.get_user_info(user_id)
    
    return render_template("medtech/patient.html", labrequests=labrequest_data, info=medtech_info, socketio=socketio)

@medtech_bp.route('/laboratory_report/')
@login_required
@role_required('medtech')
def laboratory_report():
    form=PatientForm()
    patient_id = None

    order_id = request.args.get('order_id')
    report_id = request.args.get('report_id')
    user_id = current_user.id
    medtech_info = medtech.get_user_info(user_id)
    labreq_info = medtech.get_labrequest_data(order_id)
    labrep_info = medtech.get_labreport_info(report_id)
    hematology_info = medtech.get_hematology_data(order_id)
    bacteriology_info = medtech.get_bacteriology_data(order_id)
    histopathology_info = medtech.get_histopathology_data(order_id)
    microscopy_info = medtech.get_microscopy_data(order_id)
    serology_info = medtech.get_serology_data(order_id)
    immunochem_info = medtech.get_immunochem_data(order_id)
    clinicalchem_info = medtech.get_clinicalchem_data(order_id)
    print('labrep_info:', labrep_info)
    
    return render_template("medtech/laboratory_report.html", labreq=labreq_info, PatientForm=form, 
                               patient_id=patient_id, hematology=hematology_info, bacteriology=bacteriology_info,
                               histopathology=histopathology_info, microscopy=microscopy_info, serology=serology_info,
                               immunochem=immunochem_info, clinicalchem=clinicalchem_info, report=labrep_info, info=medtech_info, socketio=socketio)

@medtech_bp.route('/profile/')
@login_required
@role_required('medtech')
def profile():
    user_id = current_user.id
    medtech_info = medtech.get_user_info(user_id)
    return render_template("medtech/profile.html", info=medtech_info, socketio=socketio)

@medtech_bp.route('/logout/')
@login_required
def logout():
    print("Logout route accessed")  
    logout_user()
    return redirect(url_for('login'))