from flask import render_template, redirect, request, url_for
from app.forms.receptionist_f import *
import app.models as models
from app.models.receptionist_m import *
from flask import Blueprint
from flask_login import login_required, logout_user, current_user
from app.routes.utils import role_required

receptionist_bp = Blueprint('receptionist', __name__)

@receptionist_bp.route('/')
@login_required
@role_required('receptionist')
def dashboard():
    current_id = current_user.id 
    receptionist_info = receptionist.get_user(current_id)
    return render_template("receptionist/dashboard.html", info=receptionist_info)

@receptionist_bp.route('/calendar/')
@login_required
@role_required('receptionist')
def calendar():
    current_id = current_user.id 
    receptionist_info = receptionist.get_user(current_id)
    return render_template("receptionist/calendar.html", info=receptionist_info)

@receptionist_bp.route('/appointment/')
@login_required
@role_required('receptionist')
def appointment():
    current_id = current_user.id 
    receptionist_info = receptionist.get_user(current_id)
    return render_template("receptionist/appointment.html", info=receptionist_info)

@receptionist_bp.route('/schedule/')
@login_required
@role_required('receptionist')
def schedule():
    current_id = current_user.id 
    receptionist_info = receptionist.get_user(current_id)
    return render_template("receptionist/schedule.html", info=receptionist_info)

@receptionist_bp.route('/patient/')
@login_required
@role_required('receptionist')
def patient():
    current_id = current_user.id 
    receptionist_info = receptionist.get_user(current_id)
    patients_data = receptionist.get_patients()

    return render_template("receptionist/patient.html", patients=patients_data, info=receptionist_info)

@receptionist_bp.route('/add_patient/', methods=["GET", "POST"])
@login_required
@role_required('receptionist')
def add_patient():
    form = PatientForm()
    current_id = current_user.id 
    receptionist_info = receptionist.get_user(current_id)

    if request.method == 'POST':
        receptionist_info = receptionist.get_user(current_id)
        fName = form.first_name.data.upper()
        mName = form.middle_name.data.upper()
        lname = form.last_name.data.upper()
        age = form.age.data
        status = form.civil_status.data
        sex = form.gender.data
        blood = form.bloodType.data
        religion = form.religion.data
        bPlace = form.birth_place.data.upper()
        bDate = form.birth_date.data
        job = form.occupation.data
        emailAdd = form.email.data
        p_num = form.contact_num.data
        cAddress = form.p_address.data.upper()
        p_nationality = form.nationality.data
        e_person = form.e_person.data.upper()
        relationship = form.relationship.data
        e_number = form.e_number.data

        new_patient = receptionist()
        new_patient.firstName = fName
        new_patient.midName = mName
        new_patient.lastName = lname
        new_patient.age = age
        new_patient.civilStatus = status
        new_patient.gender = sex
        new_patient.bloodType = blood
        new_patient.religion = religion
        new_patient.birthPlace = bPlace
        new_patient.birthDate = bDate
        new_patient.occupation = job
        new_patient.p_email = emailAdd
        new_patient.p_contactNum = p_num
        new_patient.p_address = cAddress
        new_patient.nationality = p_nationality
        new_patient.eContactName = e_person
        new_patient.relationship = relationship
        new_patient.eContactNum = e_number

        result = new_patient.add()

        if result:
            return render_template("receptionist/add_patient.html", success=True, PatientForm=form, info=receptionist_info)
        else:
            return render_template("receptionist/add_patient.html", error=True, PatientForm=form, info=receptionist_info)

    return render_template("receptionist/add_patient.html", info=receptionist_info, PatientForm=form)

# UPDATE PATIENT INFORMATION
@receptionist_bp.route('/patient_record/', methods=['GET', 'POST'])
@login_required
@role_required('receptionist')
def patient_record():
    form = PatientForm()
    current_id = current_user.id 

    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        patient_info = receptionist.get_patient_info(patient_id)
        receptionist_info = receptionist.get_user(current_id)

        return render_template('receptionist/patient_record.html', patient=patient_info, patient_id=patient_id, PatientForm=form, info=receptionist_info)

    elif request.method == 'POST':
        receptionist_info = receptionist.get_user(current_id)
        new_patient_id = request.form.get('patient_id')
        new_first_name = form.first_name.data.upper()
        new_middle_name = form.middle_name.data.upper()
        new_last_name = form.last_name.data.upper()
        new_age = form.age.data
        new_civil_status = form.civil_status.data 
        new_gender = form.gender.data
        new_bloodType = form.bloodType.data  
        new_religion = form.religion.data
        new_birth_place = form.birth_place.data.upper()  
        new_birth_date = form.birth_date.data
        new_occupation = form.occupation.data.upper() 
        new_email = form.email.data
        new_contact_num = form.contact_num.data
        new_p_address = form.p_address.data.upper()
        new_nationality = form.nationality.data
        new_e_person = form.e_person.data.upper()
        new_relationship = form.relationship.data  
        new_e_number = form.e_number.data
        
        updated = receptionist.update_patient_info(patientID=new_patient_id, firstName=new_first_name, midName=new_middle_name, lastName=new_last_name, age=new_age, 
                                             civilStatus=new_civil_status, gender=new_gender, bloodType=new_bloodType, religion=new_religion, birthPlace=new_birth_place, 
                                             occupation=new_occupation, p_email=new_email, p_contactNum=new_contact_num, birthDate=new_birth_date, p_address=new_p_address, 
                                             nationality=new_nationality, eContactName=new_e_person, relationship=new_relationship, eContactNum=new_e_number)  
        
        print('New Patient ID:', new_patient_id)

        updated_info = receptionist.get_patient_info(new_patient_id)
        print('Updated information:', updated_info)

        if updated:
            return render_template("receptionist/patient_record.html", new_patient_id=new_patient_id, success=True, patient=updated_info, PatientForm=form, info=receptionist_info)
        else:
            return render_template("receptionist/patient_record.html", new_patient_id=new_patient_id, error=True, patient=updated_info, PatientForm=form, info=receptionist_info)

    return render_template("receptionist/patient_record.html", PatientForm=form, info=receptionist_info)

# DELETE PATIENT RECORD
@receptionist_bp.route('/delete_patient/', methods=['GET', 'POST'])
@login_required
@role_required('receptionist')
def delete_patient():
    form = PatientForm()
    current_id = current_user.id 
    receptionist_info = receptionist.get_user(current_id)

    if request.method == "POST":
        patient_id = request.form.get("patient_id")
        receptionist_info = receptionist.get_user(current_id)

        result = receptionist.delete_patient_record(patient_id)

        if result:
            return render_template("receptionist/patient.html", success=True, PatientForm=form, info=receptionist_info)
        else:
            return render_template("receptionist/patient.html", error=True, PatientForm=form, info=receptionist_info)
        
    return render_template("receptionist/patient.html", PatientForm=form, info=receptionist_info)

@receptionist_bp.route('/profile/')
@login_required
@role_required('receptionist')
def profile():
    current_id = current_user.id 
    receptionist_info = receptionist.get_user(current_id)
    return render_template("receptionist/profile.html", info=receptionist_info)

@receptionist_bp.route('/logout/')
@login_required
def logout():
    print("Logout route accessed")  
    logout_user()
    return redirect(url_for('login'))