from flask import render_template, request, jsonify
from app.forms.medtech_f import *
import app.models as models
from app.models.medtech_m import *
from flask import Blueprint
from flask_login import login_required, logout_user
from app.routes.utils import role_required

medtech_bp = Blueprint('medtech', __name__)

# LAB REQUEST TABLE
@medtech_bp.route('/')
@login_required
@role_required('medtech')
def dashboard():
    labrequest_data = medtech.get_lab_requests()
    return render_template("medtech/dashboard.html", labrequests=labrequest_data)

@medtech_bp.route('/laboratory_test/', methods=['GET', 'POST'])
def laboratory_test():
    form=PatientForm()
    patient_id = None

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
        
        print('THIS IS THE PATIENT ID:', patient_id)
        print('THIS IS THE PATIENT INFORMATION:', labreq_info)
        return render_template('medtech/laboratory_test.html', labreq=labreq_info, PatientForm=form, 
                               patient_id=patient_id, hematology=hematology_info, bacteriology=bacteriology_info,
                               histopathology=histopathology_info, microscopy=microscopy_info, serology=serology_info,
                               immunochem=immunochem_info, clinicalchem=clinicalchem_info,)
    
    elif request.method == 'POST':
        data = request.get_json()
        new_order_id = data.get('order_id')
        new_patient_id = data.get('patient_id')
        extracted_values = data.get('data')

        print('THIS IS THE ORDER ID:', new_order_id)
        print('THIS IS THE NEW PATIENT ID:', new_patient_id)
        print('Received data:', extracted_values)
        
        success = True
        for item in extracted_values:
            process_name = item['processName']
            test_result = item['testResult']
            ref_value = item['referenceValue']
            diagnosis_report = item['diagnosisSummary']

            report = medtech.add_laboratory_report(orderID=new_order_id, processName=process_name, testResult=test_result, refValue=ref_value, diagnosisReport=diagnosis_report)
            print('REPORT:', report)
            if not report:
                success = False

        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': True}), 500  
        
    return render_template("medtech/laboratory_test.html", patient_id=patient_id)

@medtech_bp.route('/patient')
@login_required
@role_required('medtech')
def patient():
    labrequest_data = medtech.get_lab_reports()
    return render_template("medtech/patient.html", labrequests=labrequest_data)

@medtech_bp.route('/laboratory_report/')
def laboratory_report():
    form=PatientForm()
    patient_id = None

    order_id = request.args.get('order_id')
    patient_id = request.args.get('patient_id')
    report_id = request.args.get('report_id')
    print("report id:", report_id)
    labreq_info = medtech.get_labrequest_data(order_id)
    hematology_info = medtech.get_hematology_data(order_id)
    bacteriology_info = medtech.get_bacteriology_data(order_id)
    histopathology_info = medtech.get_histopathology_data(order_id)
    microscopy_info = medtech.get_microscopy_data(order_id)
    serology_info = medtech.get_serology_data(order_id)
    immunochem_info = medtech.get_immunochem_data(order_id)
    clinicalchem_info = medtech.get_clinicalchem_data(order_id)
    lab_report = medtech.get_lab_report(report_id)
    print('lab report:', lab_report)
    
    return render_template("medtech/laboratory_report.html", labreq=labreq_info, PatientForm=form, 
                               patient_id=patient_id, hematology=hematology_info, bacteriology=bacteriology_info,
                               histopathology=histopathology_info, microscopy=microscopy_info, serology=serology_info,
                               immunochem=immunochem_info, clinicalchem=clinicalchem_info, reports=lab_report)

@medtech_bp.route('/profile')
@login_required
@role_required('medtech')
def profile():
    return render_template("medtech/profile.html")

@medtech_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))