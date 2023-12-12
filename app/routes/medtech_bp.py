from flask import render_template, request, jsonify, redirect, url_for
from app.forms.medtech_f import *
import app.models as models
from app.models.medtech_m import *
from flask import Blueprint
from flask_login import login_required, logout_user, current_user
from app.routes.utils import role_required

medtech_bp = Blueprint('medtech', __name__)

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
                               immunochem=immunochem_info, clinicalchem=clinicalchem_info, medtech=user_info)
    
    elif request.method == 'POST':
        data = request.get_json()
        new_order_id = data.get('order_id')
        new_patient_id = data.get('patient_id')
        new_medtech_name = data.get('medtech_name')
        extracted_values = data.get('data')

        print('THIS IS THE ORDER ID:', new_order_id)
        print('THIS IS THE NEW PATIENT ID:', new_patient_id)
        print('THIS IS THE NEW MEDTECH NAME:', new_medtech_name)
        print('Received data:', extracted_values)
        
        success = True
        for item in extracted_values:
            process_name = item['processName']
            test_result = item['testResult']
            ref_value = item['referenceValue']
            diagnosis_report = item['diagnosisSummary']

            report = medtech.add_laboratory_report(orderID=new_order_id, medtech=new_medtech_name, processName=process_name, testResult=test_result, refValue=ref_value, diagnosisReport=diagnosis_report)
            print('REPORT:', report)
            if not report:
                success = False

        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': True}), 500  
        
    return render_template("medtech/laboratory_test.html", patient_id=patient_id, medtech=user_info)

@medtech_bp.route('/patient/')
@login_required
@role_required('medtech')
def patient():
    user_id = current_user.id
    labrequest_data = medtech.get_lab_reports()
    medtech_info = medtech.get_user_info(user_id)
    
    return render_template("medtech/patient.html", labrequests=labrequest_data, info=medtech_info)

@medtech_bp.route('/laboratory_report/')
@login_required
@role_required('medtech')
def laboratory_report():
    form=PatientForm()
    patient_id = None

    order_id = request.args.get('order_id')
    patient_id = request.args.get('patient_id')
    report_id = request.args.get('report_id')
    user_id = current_user.id
    medtech_info = medtech.get_user_info(user_id)

    labreq_info = medtech.get_labrequest_data(order_id)
    labrep_info = medtech.get_labreport_info(report_id)
    lab_report = medtech.get_lab_report(report_id)
    hematology_info = medtech.get_hematology_data(order_id)
    bacteriology_info = medtech.get_bacteriology_data(order_id)
    histopathology_info = medtech.get_histopathology_data(order_id)
    microscopy_info = medtech.get_microscopy_data(order_id)
    serology_info = medtech.get_serology_data(order_id)
    immunochem_info = medtech.get_immunochem_data(order_id)
    clinicalchem_info = medtech.get_clinicalchem_data(order_id)
    
    return render_template("medtech/laboratory_report.html", labreq=labreq_info, PatientForm=form, 
                               patient_id=patient_id, hematology=hematology_info, bacteriology=bacteriology_info,
                               histopathology=histopathology_info, microscopy=microscopy_info, serology=serology_info,
                               immunochem=immunochem_info, clinicalchem=clinicalchem_info, reports=lab_report, report=labrep_info, info=medtech_info)

@medtech_bp.route('/profile/')
@login_required
@role_required('medtech')
def profile():
    user_id = current_user.id
    medtech_info = medtech.get_user_info(user_id)
    return render_template("medtech/profile.html", info=medtech_info)

@medtech_bp.route('/logout/')
@login_required
def logout():
    print("Logout route accessed")  
    logout_user()
    return redirect(url_for('login'))