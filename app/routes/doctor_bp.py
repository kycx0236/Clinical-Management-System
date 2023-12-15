from flask import render_template, request, jsonify, redirect, url_for, flash
from app.forms.doctor_f import *
import app.models as models
from app.models.doctor_m import *
import math
import secrets
import string
from flask import Blueprint
from app.forms.doctor_f import AppointmentForm, EditAppointmentForm
from flask_login import login_required, logout_user, current_user
from app.routes.utils import role_required

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/')
@login_required
@role_required('doctor')
def dashboard():
    return render_template("doctor/dashboard/dashboard.html")

@doctor_bp.route('/calendar/')
@login_required
@role_required('doctor')
def calendar():
    return render_template("doctor/calendar/calendar.html")

headings = ("Reference Number", "Date", "Time", "Last Name", "Status", "Doctor", "Actions")

@doctor_bp.route('/appointment/')
@login_required
@role_required('doctor')
def appointment():
    user_id = current_user.id
    print("Inside appointment function: ",user_id)
    form = EditAppointmentForm()
    # Get the page number from the query string, default to 1 if not specified
    page = int(request.args.get('page', 1))

    # Set the number of items to display per page
    items_per_page = 9  # You can adjust this to your preferred value

    # Retrieve all appointment data from your model
    all_appointments = Appointment.all(user_id)

    # Calculate the total number of pages
    total_pages = math.ceil(len(all_appointments) / items_per_page)

    # Calculate the starting and ending index for the current page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    # Get the data for the current page
    data = all_appointments[start_index:end_index]

    # Convert appointment data to a list of dictionaries for easy JSON serialization
    data_dict = [
        {
            'reference_number': appointment[0],
            'date_appointment': appointment[1],
            'time_appointment': str(appointment[2]),  # Ensure time_appointment is treated as a string
            'last_name': appointment[3],
            'status_': appointment[4],
            'doctorName': appointment[5],
        }
        for appointment in data
    ]

    return render_template("doctor/appointment/appointment.html", headings=headings, data=data_dict, page=page, total_pages=total_pages, form=form)

@doctor_bp.route('/profile/')
@login_required
@role_required('doctor')
def profile():
    return render_template("doctor/profile/profile.html")

@doctor_bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# -------------------------------------------- PATIENT -------------------------------------------- #
# ADD PATIENT INFORMATION
@doctor_bp.route('/add/', methods=["GET", "POST"])
@login_required
@role_required('doctor')
def add_patient():
    form = PatientForm()
    user_id = current_user.id

    if request.method == 'POST':
        fName = request.form.get("first_name").upper()
        mName = request.form.get("middle_name").upper()
        lname = request.form.get("last_name").upper()
        age = int(request.form.get("age"))
        status = request.form.get("civil_status")
        sex = request.form.get("gender")
        blood = request.form.get("bloodType")
        religion = request.form.get("religion")
        bPlace = request.form.get("birth_place").upper()
        bDate = request.form.get("birth_date")
        job = request.form.get("occupation").upper()
        emailAdd = request.form.get("email")
        p_num = ''.join(filter(str.isdigit, request.form.get("contact_num")))
        cAddress = request.form.get("p_address").upper()
        p_nationality = request.form.get("nationality")
        e_person = request.form.get("e_person").upper()
        relationship = request.form.get("relationship")
        e_number = ''.join(filter(str.isdigit, request.form.get("e_number")))
        
        new_patient = doctor()
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

        result = new_patient.add(user_id)

        if result:
            return render_template("doctor/patient/add_patient.html", success=True, PatientForm=form)
        else:
            return render_template("doctor/patient/add_patient.html", error=True, PatientForm=form)

    return render_template("doctor/patient/add_patient.html", PatientForm=form)

# ADD AND UPDATE MEDICAL HISTORY
@doctor_bp.route('/medical_history/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def medical_history():
    form = PatientForm()
    patient_id = None

    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        patient_info = doctor.get_patient_history (patient_id)
        print('THIS IS THE PATIENT ID:', patient_id)
        print('THIS IS THE PATIENT INFORMATION:', patient_info)
        return render_template('doctor/patient/medical_history.html', patient=patient_info, PatientForm=form, patient_id=patient_id)

    elif request.method == 'POST':
        new_history_id = request.form.get('history_id')
        new_patient_id = request.form.get('patient_id')
        print('THIS IS THE NEW PATIENT ID:', new_patient_id)

    # IMMUNIZATION
        bcg_checkbox_value = 1 if request.form.get('bcgCheckbox') == 'checked' else 0
        dtp_checkbox_value = 1 if request.form.get('dtpCheckbox') == 'checked' else 0
        pcv_checkbox_value = 1 if request.form.get('pcvCheckbox') == 'checked' else 0
        influenza_checkbox_value = 1 if request.form.get('influenzaCheckbox') == 'checked' else 0
        hepa_checkbox_value = 1 if request.form.get('hepaCheckbox') == 'checked' else 0
        ipv_checkbox_value = 1 if request.form.get('ipvCheckbox') == 'checked' else 0
        mmr_checkbox_value = 1 if request.form.get('mmrCheckbox') == 'checked' else 0
        hpv_checkbox_value = 1 if request.form.get('hpvCheckbox') == 'checked' else 0

    # FAMILY HISTORY
        asthma_checkbox_value = 1 if request.form.get('asthmaCheckbox') == 'checked' else 0
        diabetes_checkbox_value = 1 if request.form.get('diabetesCheckbox') == 'checked' else 0
        heart_checkbox_value = 1 if request.form.get('heartCheckbox') == 'checked' else 0
        birth_checkbox_value = 1 if request.form.get('birthCheckbox') == 'checked' else 0
        bone_checkbox_value = 1 if request.form.get('boneCheckbox') == 'checked' else 0
        alzheimer_checkbox_value = 1 if request.form.get('alzheimerCheckbox') == 'checked' else 0
        cancer_checkbox_value = 1 if request.form.get('cancerCheckbox') == 'checked' else 0
        thyroid_checkbox_value = 1 if request.form.get('thyroidCheckbox') == 'checked' else 0
        tuberculosis_checkbox_value = 1 if request.form.get('tuberculosisCheckbox') == 'checked' else 0
        eye_checkbox_value = 1 if request.form.get('eyeCheckbox') == 'checked' else 0
        clots_checkbox_value = 1 if request.form.get('clotsCheckbox') == 'checked' else 0
        mental_checkbox_value = 1 if request.form.get('mentalCheckbox') == 'checked' else 0
        kidney_checkbox_value = 1 if request.form.get('kidneyCheckbox') == 'checked' else 0
        anemia_checkbox_value = 1 if request.form.get('anemiaCheckbox') == 'checked' else 0
        muscle_checkbox_value = 1 if request.form.get('muscleCheckbox') == 'checked' else 0
        highblood_checkbox_value = 1 if request.form.get('highbloodCheckbox') == 'checked' else 0
        epilepsy_checkbox_value = 1 if request.form.get('epilepsyCheckbox') == 'checked' else 0
        skin_checkbox_value = 1 if request.form.get('skinCheckbox') == 'checked' else 0
        hiv_checkbox_value = 1 if request.form.get('hivCheckbox') == 'checked' else 0
        pulmonary_checkbox_value = 1 if request.form.get('pulmonaryCheckbox') == 'checked' else 0
        new_specifications = request.form.get('specifications').upper()
        new_others = request.form.get('others').upper()

    # PAST HISTORY
        new_past1 = request.form.get('past_c1').upper()
        new_medication1 = request.form.get('medication1').upper()
        new_dosage1 = request.form.get('dosage1').upper()
        new_hdate1 = request.form.get('h_date1')
        if not new_hdate1:
            new_hdate1 = None 
        new_past2 = request.form.get('past_c2').upper()
        new_medication2 = request.form.get('medication2').upper()
        new_dosage2 = request.form.get('dosage2').upper()
        new_hdate2 = request.form.get('h_date2')
        if not new_hdate2:
            new_hdate2 = None
        new_past3 = request.form.get('past_c3').upper()
        new_medication3 = request.form.get('medication3').upper()
        new_dosage3 = request.form.get('dosage3').upper()
        new_hdate3 = request.form.get('h_date3')
        if not new_hdate3:
            new_hdate3 = None

    # SOCIAL HISTORY 
        habit = request.form.get('habitually')
        yDrunk = request.form.get('yearsDrunk')
        if yDrunk and yDrunk.isdigit():
            yDrunk = int(yDrunk)
        else:
            yDrunk = None
        fDrink = request.form.get('frequencyDrink').upper()
        qDrink = request.form.get('quitDrinking')
        if qDrink and qDrink.isdigit():
            qDrink = int(qDrink)
        else:
            qDrink = None
        frequent = request.form.get('frequently')
        ySmoked = request.form.get('yearsSmoked')
        if ySmoked and ySmoked.isdigit():
            ySmoked = int(ySmoked)
        else:
            ySmoked = None
        fSmoke = request.form.get('frequencySmoke').upper()
        qSmoke = request.form.get('quitSmoking')
        if qSmoke and qSmoke.isdigit():
            qSmoke = int(qSmoke)
        else:
            qSmoke = None
        often = request.form.get('often')
        eType = request.form.get('exerciseType').upper()
        fExercise = request.form.get('frequencyExercise').upper()
        dActivity = request.form.get('durationActivity').upper()
        sActive = request.form.get('sexActive')
        sPartner = request.form.get('sexPartner')
        nSPartner = request.form.get('numSexPartner')
        if nSPartner and nSPartner.isdigit():
            nSPartner = int(nSPartner)
        else:
            nSPartner = None
        contraceptions = request.form.get('contraception').upper()
        use = request.form.get('useDrugs')
        sDrugs = request.form.get('specifyDrugs').upper()
        fDrugs = request.form.get('frequencyDrugs').upper()
        diet = request.form.get('diet').upper()

    # SURGICAL HISTORY  
        sDate1 = request.form.get('surgeryDate1')
        if not sDate1:
            sDate1 = None
        sProcedure1 = request.form.get('surgeryProcedure1').upper()
        shospital1 = request.form.get('hospital1').upper()
        sDate2 = request.form.get('surgeryDate2')
        if not sDate2:
            sDate2 = None
        sProcedure2 = request.form.get('surgeryProcedure2').upper()
        shospital2 = request.form.get('hospital2').upper()
        sDate3 = request.form.get('surgeryDate3')
        if not sDate3:
            sDate3 = None
        sProcedure3 = request.form.get('surgeryProcedure3').upper()
        shospital3 = request.form.get('hospital3').upper()

    # MEDICATIONS
        meds = request.form.get('medications').upper()

    # ALLERGIES
        allergy = request.form.get('allergies').upper()

        existing_history = doctor.get_patient_history(new_patient_id)
        print('EXISTING HISTORY:', existing_history)
        
        if existing_history:
            updated = doctor.update_medical_history(historyID = new_history_id, patientID = new_patient_id, bcgCheckbox = bcg_checkbox_value,
                                                dtpCheckbox = dtp_checkbox_value, pcvCheckbox = pcv_checkbox_value, influenzaCheckbox = influenza_checkbox_value,
                                                hepaCheckbox = hepa_checkbox_value, ipvCheckbox = ipv_checkbox_value, mmrCheckbox = mmr_checkbox_value,
                                                hpvCheckbox = hpv_checkbox_value, asthmaCheckbox = asthma_checkbox_value,diabetesCheckbox = diabetes_checkbox_value,
                                                heartCheckbox = heart_checkbox_value, birthCheckbox = birth_checkbox_value, boneCheckbox = bone_checkbox_value,
                                                alzheimerCheckbox = alzheimer_checkbox_value, cancerCheckbox = cancer_checkbox_value, thyroidCheckbox = thyroid_checkbox_value,
                                                tuberculosisCheckbox = tuberculosis_checkbox_value, eyeCheckbox = eye_checkbox_value, clotsCheckbox = clots_checkbox_value,
                                                mentalCheckbox = mental_checkbox_value, kidneyCheckbox = kidney_checkbox_value,anemiaCheckbox = anemia_checkbox_value,
                                                muscleCheckbox = muscle_checkbox_value, highbloodCheckbox = highblood_checkbox_value, epilepsyCheckbox = epilepsy_checkbox_value,
                                                skinCheckbox = skin_checkbox_value, hivCheckbox = hiv_checkbox_value, pulmonaryCheckbox = pulmonary_checkbox_value,
                                                specifications = new_specifications, others = new_others, past_c1 = new_past1, medication1 = new_medication1,
                                                dosage1 = new_dosage1, h_date1 = new_hdate1, past_c2 = new_past2, medication2 = new_medication2, dosage2 = new_dosage2,
                                                h_date2 = new_hdate2, past_c3 = new_past3, medication3 = new_medication3, dosage3 = new_dosage3, h_date3 = new_hdate3,
                                                habitually = habit, yearsDrunk = yDrunk, frequencyDrink = fDrink, quitDrinking = qDrink, frequently = frequent,
                                                yearsSmoked = ySmoked, frequencySmoke = fSmoke, quitSmoking = qSmoke, often = often, exerciseType = eType,
                                                frequencyExercise = fExercise, durationActivity = dActivity, sexActive = sActive, sexPartner = sPartner,
                                                numSexPartner = nSPartner, contraception = contraceptions, useDrugs = use, specifyDrugs = sDrugs, frequencyDrugs = fDrugs,
                                                surgeryDate1 = sDate1, surgeryProcedure1 = sProcedure1, hospital1 = shospital1, surgeryDate2 = sDate2,
                                                surgeryProcedure2 = sProcedure2, hospital2 = shospital2, surgeryDate3 = sDate3, surgeryProcedure3 = sProcedure3,
                                                hospital3 = shospital3, medications = meds, allergies = allergy, diet=diet)  
            
            updated_info = doctor.get_patient_history(new_patient_id)
            print('UPDATED INFO:', updated_info)
            
            if updated:
                return render_template("doctor/patient/medical_history.html", new_patient_id=new_patient_id, success=True, patient=updated_info, PatientForm=form)
            else:
                return render_template("doctor/patient/medical_history.html", new_patient_id=new_patient_id, error=True, patient=updated_info, PatientForm=form)

        else:
            result = doctor.add_medical_history(patientID = new_patient_id, bcgCheckbox = bcg_checkbox_value,
                                                dtpCheckbox = dtp_checkbox_value, pcvCheckbox = pcv_checkbox_value, influenzaCheckbox = influenza_checkbox_value,
                                                hepaCheckbox = hepa_checkbox_value, ipvCheckbox = ipv_checkbox_value, mmrCheckbox = mmr_checkbox_value,
                                                hpvCheckbox = hpv_checkbox_value, asthmaCheckbox = asthma_checkbox_value,diabetesCheckbox = diabetes_checkbox_value,
                                                heartCheckbox = heart_checkbox_value, birthCheckbox = birth_checkbox_value, boneCheckbox = bone_checkbox_value,
                                                alzheimerCheckbox = alzheimer_checkbox_value, cancerCheckbox = cancer_checkbox_value, thyroidCheckbox = thyroid_checkbox_value,
                                                tuberculosisCheckbox = tuberculosis_checkbox_value, eyeCheckbox = eye_checkbox_value, clotsCheckbox = clots_checkbox_value,
                                                mentalCheckbox = mental_checkbox_value, kidneyCheckbox = kidney_checkbox_value,anemiaCheckbox = anemia_checkbox_value,
                                                muscleCheckbox = muscle_checkbox_value, highbloodCheckbox = highblood_checkbox_value, epilepsyCheckbox = epilepsy_checkbox_value,
                                                skinCheckbox = skin_checkbox_value, hivCheckbox = hiv_checkbox_value, pulmonaryCheckbox = pulmonary_checkbox_value,
                                                specifications = new_specifications, others = new_others, past_c1 = new_past1, medication1 = new_medication1,
                                                dosage1 = new_dosage1, h_date1 = new_hdate1, past_c2 = new_past2, medication2 = new_medication2, dosage2 = new_dosage2,
                                                h_date2 = new_hdate2, past_c3 = new_past3, medication3 = new_medication3, dosage3 = new_dosage3, h_date3 = new_hdate3,
                                                habitually = habit, yearsDrunk = yDrunk, frequencyDrink = fDrink, quitDrinking = qDrink, frequently = frequent,
                                                yearsSmoked = ySmoked, frequencySmoke = fSmoke, quitSmoking = qSmoke, often = often, exerciseType = eType,
                                                frequencyExercise = fExercise, durationActivity = dActivity, sexActive = sActive, sexPartner = sPartner,
                                                numSexPartner = nSPartner, contraception = contraceptions, useDrugs = use, specifyDrugs = sDrugs, frequencyDrugs = fDrugs,
                                                surgeryDate1 = sDate1, surgeryProcedure1 = sProcedure1, hospital1 = shospital1, surgeryDate2 = sDate2,
                                                surgeryProcedure2 = sProcedure2, hospital2 = shospital2, surgeryDate3 = sDate3, surgeryProcedure3 = sProcedure3,
                                                hospital3 = shospital3, medications = meds, allergies = allergy, diet=diet)
            
            updated_info = doctor.get_patient_history(new_patient_id)
            print('NEW PATIENT HISTORY:', updated_info)

            if result:
                return render_template("doctor/patient/medical_history.html", patient_id=patient_id, success=True, patient=updated_info, PatientForm=form)
            else:
                return render_template("doctor/patient/medical_history.html", patient_id=patient_id, error=True, patient=updated_info, PatientForm=form)

    return render_template("doctor/patient/medical_history.html", patient_id=patient_id, PatientForm=form)

# ADD MEDICAL ASSESSMENT FOR EACH APPOINTMENT
@doctor_bp.route('/add_assessment/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def add_assessment():
    form = PatientForm()
    patient_id = None

    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        patient_info = doctor.get_patient_info(patient_id)
        return render_template('doctor/patient/add_assessment.html', patient=patient_info, PatientForm=form, patient_id=patient_id)
    
    elif request.method == 'POST':
        new_patient_id = request.form.get('patient_id')
        print('THIS IS THE NEW PATIENT ID:', new_patient_id)

    # COMPLAINT
        sub = request.form.get('subject').upper()
        complain = request.form.get('complaints').upper()

    # HISTORY OF PRESENT ILLNESS
        p_illness = request.form.get('h_illness').upper()

    # VITAL SIGNS
        blood_p = request.form.get('blood_p').upper()
        pulse_r = request.form.get('pulse_r').upper()
        temp = request.form.get('temp').upper()
        respiratory_r = request.form.get('respiratory_r').upper()
        height = request.form.get('height')
        weight = request.form.get('weight')
        body_mass = request.form.get('body_mass')
        oxygenSaturation = request.form.get('oxygenSaturation').upper()
        painSection = request.form.get('painSection').upper()

    # PHYSICAL EXAMINATIONS
        normal_head = request.form.get('normal_head').upper()
        abnormalities_head = request.form.get('abnormalities_head').upper()
        normal_ears = request.form.get('normal_ears').upper()
        abnormalities_ears = request.form.get('abnormalities_ears').upper()
        normal_eyes = request.form.get('normal_eyes').upper()
        abnormalities_eyes = request.form.get('abnormalities_eyes').upper()
        normal_nose = request.form.get('normal_nose').upper()
        abnormalities_nose = request.form.get('abnormalities_nose').upper()
        normal_skin = request.form.get('normal_skin').upper()
        abnormalities_skin = request.form.get('abnormalities_skin').upper()
        normal_back = request.form.get('normal_back').upper()
        abnormalities_back = request.form.get('abnormalities_back').upper()
        normal_neck = request.form.get('normal_neck').upper()
        abnormalities_neck = request.form.get('abnormalities_neck').upper()
        normal_throat = request.form.get('normal_throat').upper()
        abnormalities_throat = request.form.get('abnormalities_throat').upper()
        normal_chest = request.form.get('normal_chest').upper()
        abnormalities_chest = request.form.get('abnormalities_chest').upper()
        normal_abdomen = request.form.get('normal_abdomen').upper()
        abnormalities_abdomen = request.form.get('abnormalities_abdomen').upper()
        normal_upper = request.form.get('normal_upper').upper()
        abnormalities_upper = request.form.get('abnormalities_upper').upper()
        normal_lower = request.form.get('normal_lower').upper()
        abnormalities_lower = request.form.get('abnormalities_lower').upper()
        normal_tract = request.form.get('normal_tract').upper()
        abnormalities_tract = request.form.get('abnormalities_tract').upper()
        comments = request.form.get('comments').upper()

    # DIAGNOSIS
        diagnosis = request.form.get('diagnosis').upper()

        result = doctor.add_medical_assessment(patientID=new_patient_id, subjectComp=sub, complaints=complain, illnessHistory=p_illness, bloodPressure=blood_p,
                                               pulseRate=pulse_r, temperature=temp, respRate=respiratory_r, height=height, weight_p=weight, bmi=body_mass, normal_head=normal_head,
                                               abnormalities_head=abnormalities_head, normal_ears=normal_ears, abnormalities_ears=abnormalities_ears, normal_eyes=normal_eyes
                                               , abnormalities_eyes=abnormalities_eyes, normal_nose=normal_nose, abnormalities_nose=abnormalities_nose, normal_skin=normal_skin
                                               , abnormalities_skin=abnormalities_skin, normal_back=normal_back, abnormalities_back=abnormalities_back, normal_neck=normal_neck
                                               , abnormalities_neck=abnormalities_neck, normal_throat=normal_throat, abnormalities_throat=abnormalities_throat, normal_chest=normal_chest
                                               , abnormalities_chest=abnormalities_chest, normal_abdomen=normal_abdomen, abnormalities_abdomen=abnormalities_abdomen, normal_upper=normal_upper
                                               , abnormalities_upper=abnormalities_upper, normal_lower=normal_lower, abnormalities_lower=abnormalities_lower, normal_tract=normal_tract
                                               , abnormalities_tract=abnormalities_tract, comments=comments, diagnosis=diagnosis, oxygenSaturation=oxygenSaturation, painSection=painSection)
            
        new_consultation = doctor.get_patient_info(new_patient_id)
        print('NEW ASSESSMENT:', new_consultation)

        if result:
            return render_template("doctor/patient/add_assessment.html", patient_id=patient_id, success=True, patient=new_consultation, PatientForm=form)
        else:
            return render_template("doctor/patient/add_assessment.html", patient_id=patient_id, error=True, patient=new_consultation, PatientForm=form)

    return render_template("doctor/patient/add_assessment.html", patient_id=patient_id, PatientForm=form)

# PATIENT TABLE
@doctor_bp.route('/patient/')
@login_required
@role_required('doctor')
def patient():
    user_id = current_user.id
    print(f"Logged-in doctor ID: {user_id}")

    patients_data = doctor.get_patients(user_id)
    return render_template("doctor/patient/patient.html", patients=patients_data)

# CONSULTATION TABLE
@doctor_bp.route('/consultation/')
@login_required
@role_required('doctor')
def consultation():
    patient_id = request.args.get('patient_id')
    patient_info = doctor.get_patient_info(patient_id)
    consultation_data = doctor.get_consultations(patient_id)
    print('PATIENT ID:', patient_id)
    return render_template("doctor/patient/consultation.html", consultations=consultation_data,patient=patient_info, patient_id=patient_id)

# LAB RESULTS TABLE
@doctor_bp.route('/lab_results/')
@login_required
@role_required('doctor')
def lab_results():
    patient_id = request.args.get('patient_id')
    report_info = doctor.get_lab_reports(patient_id)
    print('patient id:', patient_id)
    print('report info:', report_info)
    return render_template("doctor/patient/lab_results.html", patient_id=patient_id, labreports=report_info)

# UPDATE PATIENT INFORMATION
@doctor_bp.route('/patient_record/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def patient_record():
    form = PatientForm()

    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        patient_info = doctor.get_patient_info(patient_id)

        return render_template('doctor/patient/patient_record.html', patient=patient_info, patient_id=patient_id, PatientForm=form)

    elif request.method == 'POST':
        new_patient_id = request.form.get('patient_id')
        new_first_name = request.form.get('first_name').upper()
        new_middle_name = request.form.get('middle_name').upper()
        new_last_name = request.form.get('last_name').upper()
        new_age = int(request.form.get("age"))    
        new_civil_status = request.form.get('civil_status')   
        new_gender = request.form.get('gender')
        new_bloodType = request.form.get('bloodType')    
        new_religion = request.form.get('religion')
        new_birth_place = request.form.get('birth_place').upper()    
        new_birth_date = request.form.get('birth_date')
        new_occupation = request.form.get('occupation').upper()    
        new_email = request.form.get('email')
        new_contact_num = ''.join(filter(str.isdigit, request.form.get("contact_num"))) 
        new_p_address = request.form.get('p_address')
        new_nationality = request.form.get('nationality')    
        new_e_person = request.form.get('e_person').upper()
        new_relationship = request.form.get('relationship')    
        new_e_number = ''.join(filter(str.isdigit, request.form.get("e_number")))

        updated = doctor.update_patient_info(patientID=new_patient_id, firstName=new_first_name, midName=new_middle_name, lastName=new_last_name, age=new_age, 
                                             civilStatus=new_civil_status, gender=new_gender, bloodType=new_bloodType, religion=new_religion, birthPlace=new_birth_place, 
                                             occupation=new_occupation, p_email=new_email, p_contactNum=new_contact_num, birthDate=new_birth_date, p_address=new_p_address, 
                                             nationality=new_nationality, eContactName=new_e_person, relationship=new_relationship, eContactNum=new_e_number)  
        
        print('New Patient ID:', new_patient_id)

        updated_info = doctor.get_patient_info(new_patient_id)
        print('Updated information:', updated_info)

        if updated:
            return render_template("doctor/patient/patient_record.html", new_patient_id=new_patient_id, success=True, patient=updated_info, PatientForm=form)
        else:
            return render_template("doctor/patient/patient_record.html", new_patient_id=new_patient_id, error=True, patient=updated_info, PatientForm=form)

    return render_template("doctor/patient/patient_record.html", PatientForm=form)


# UPDATE MEDICAL ASSESSMENT
@doctor_bp.route('/assessment/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def assessment():
    form=PatientForm()
    patient_id = None

    if request.method == 'GET':
        assessment_id = request.args.get('assessment_id')
        patient_id = request.args.get('patient_id')
        patient_info = doctor.get_consultation_info(assessment_id, patient_id)
        print('THIS IS THE ASSESSMENT ID:', assessment_id)
        print('THIS IS THE PATIENT ID:', patient_id)
        print('THIS IS THE PATIENT INFORMATION:', patient_info)
        return render_template('doctor/patient/assessment.html', patient=patient_info, PatientForm=form, patient_id=patient_id)
    
    elif request.method == 'POST':
        new_assessment_id = request.form.get('assessment_id')
        new_patient_id = request.form.get('patient_id')
        print('THIS IS THE NEW PATIENT ID:', new_patient_id)

    # COMPLAINT
        sub = request.form.get('subject').upper()
        complain = request.form.get('complaints').upper()

    # HISTORY OF PRESENT ILLNESS
        p_illness = request.form.get('h_illness').upper()

    # VITAL SIGNS
        blood_p = request.form.get('blood_p').upper()
        pulse_r = request.form.get('pulse_r').upper()
        temp = request.form.get('temp').upper()
        respiratory_r = request.form.get('respiratory_r').upper()
        height = request.form.get('height')
        weight = request.form.get('weight')
        body_mass = request.form.get('body_mass')
        oxygenSaturation = request.form.get('oxygenSaturation').upper()
        painSection = request.form.get('painSection').upper()

    # PHYSICAL EXAMINATIONS
        normal_head = request.form.get('normal_head').upper()
        abnormalities_head = request.form.get('abnormalities_head').upper()
        normal_ears = request.form.get('normal_ears').upper()
        abnormalities_ears = request.form.get('abnormalities_ears').upper()
        normal_eyes = request.form.get('normal_eyes').upper()
        abnormalities_eyes = request.form.get('abnormalities_eyes').upper()
        normal_nose = request.form.get('normal_nose').upper()
        abnormalities_nose = request.form.get('abnormalities_nose').upper()
        normal_skin = request.form.get('normal_skin').upper()
        abnormalities_skin = request.form.get('abnormalities_skin').upper()
        normal_back = request.form.get('normal_back').upper()
        abnormalities_back = request.form.get('abnormalities_back').upper()
        normal_neck = request.form.get('normal_neck').upper()
        abnormalities_neck = request.form.get('abnormalities_neck').upper()
        normal_throat = request.form.get('normal_throat').upper()
        abnormalities_throat = request.form.get('abnormalities_throat').upper()
        normal_chest = request.form.get('normal_chest').upper()
        abnormalities_chest = request.form.get('abnormalities_chest').upper()
        normal_abdomen = request.form.get('normal_abdomen').upper()
        abnormalities_abdomen = request.form.get('abnormalities_abdomen').upper()
        normal_upper = request.form.get('normal_upper').upper()
        abnormalities_upper = request.form.get('abnormalities_upper').upper()
        normal_lower = request.form.get('normal_lower').upper()
        abnormalities_lower = request.form.get('abnormalities_lower').upper()
        normal_tract = request.form.get('normal_tract').upper()
        abnormalities_tract = request.form.get('abnormalities_tract').upper()
        comments = request.form.get('comments').upper()

    # DIAGNOSIS
        diagnosis = request.form.get('diagnosis').upper()

        update = doctor.update_medical_assessment(assessmentID=new_assessment_id, patientID=new_patient_id, subjectComp=sub, complaints=complain, illnessHistory=p_illness, bloodPressure=blood_p,
                                               pulseRate=pulse_r, temperature=temp, respRate=respiratory_r, height=height, weight_p=weight, bmi=body_mass, normal_head=normal_head,
                                               abnormalities_head=abnormalities_head, normal_ears=normal_ears, abnormalities_ears=abnormalities_ears, normal_eyes=normal_eyes
                                               , abnormalities_eyes=abnormalities_eyes, normal_nose=normal_nose, abnormalities_nose=abnormalities_nose, normal_skin=normal_skin
                                               , abnormalities_skin=abnormalities_skin, normal_back=normal_back, abnormalities_back=abnormalities_back, normal_neck=normal_neck
                                               , abnormalities_neck=abnormalities_neck, normal_throat=normal_throat, abnormalities_throat=abnormalities_throat, normal_chest=normal_chest
                                               , abnormalities_chest=abnormalities_chest, normal_abdomen=normal_abdomen, abnormalities_abdomen=abnormalities_abdomen, normal_upper=normal_upper
                                               , abnormalities_upper=abnormalities_upper, normal_lower=normal_lower, abnormalities_lower=abnormalities_lower, normal_tract=normal_tract
                                               , abnormalities_tract=abnormalities_tract, comments=comments, diagnosis=diagnosis, oxygenSaturation=oxygenSaturation, painSection=painSection)
            
        new_consultation = doctor.get_consultation_info(new_assessment_id, new_patient_id)
        print('NEW ASSESSMENT:', new_consultation)

        if update:
            return render_template("doctor/patient/assessment.html", new_patient_id=new_patient_id, success=True, patient=new_consultation, PatientForm=form)
        else:
            return render_template("doctor/patient/assessment.html", new_patient_id=new_patient_id, error=True, patient=new_consultation, PatientForm=form)

    return render_template("doctor/patient/assessment.html", patient_id=patient_id, PatientForm=form)
  
# LABORATORY RESULT
@doctor_bp.route('/results/')
@login_required
@role_required('doctor')
def results():
    form=PatientForm()
    patient_id = None

    order_id = request.args.get('order_id')
    patient_id = request.args.get('patient_id')
    report_id = request.args.get('report_id')
    print("report id:", report_id)
    labreq_info = doctor.get_labrequest_data(order_id)
    labrep_info = doctor.get_labreport_info(report_id)
    lab_report = doctor.get_lab_report(report_id)
    hematology_info = doctor.get_hematology_data(order_id)
    bacteriology_info = doctor.get_bacteriology_data(order_id)
    histopathology_info = doctor.get_histopathology_data(order_id)
    microscopy_info = doctor.get_microscopy_data(order_id)
    serology_info = doctor.get_serology_data(order_id)
    immunochem_info = doctor.get_immunochem_data(order_id)
    clinicalchem_info = doctor.get_clinicalchem_data(order_id)

    return render_template("doctor/patient/results.html", labreq=labreq_info, PatientForm=form, 
                               patient_id=patient_id, hematology=hematology_info, bacteriology=bacteriology_info,
                               histopathology=histopathology_info, microscopy=microscopy_info, serology=serology_info,
                               immunochem=immunochem_info, clinicalchem=clinicalchem_info, reports=lab_report, report=labrep_info)

# REQUEST TO RUN LABORATORY TESTS
@doctor_bp.route('/labtest_request/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def labtest_request():
    form=PatientForm()
    patient_id = None

    if request.method == 'GET':
        user_id = current_user.id
        patient_id = request.args.get('patient_id')
        patient_info = doctor.get_patient_info(patient_id)
        doctor_info = doctor.get_doctor_info(user_id)

        return render_template('doctor/patient/labtest_request.html', patient=patient_info, doctor=doctor_info, PatientForm=form, patient_id=patient_id)
    
    elif request.method == 'POST':
        user_id = current_user.id
        doctor_info = doctor.get_doctor_info(user_id)
        new_patient_id = request.form.get('patient_id')

    # PATIENT INFORMATION
        patient_fullName = request.form.get('fullName')
        lab_subject = request.form.get('labsubject').upper()
        sex = request.form.get("gender")
        age = request.form.get("age")
        doctorName = request.form.get("doctorName")
        requestDate = request.form.get("dateofRequest")
        otherTest = request.form.get("others").upper()
        print('patient_fullName:', patient_fullName)
        print('doctor', doctor)
        print('sex:', sex)
        print('age:', age)
        print('requestDate:', requestDate)

    # HEMATOLOGY
        cbcplateCheckbox_value = 1 if request.form.get('cbcplateCheckbox') == 'checked' else 0
        hgbhctCheckbox = 1 if request.form.get('hgbhctCheckbox') == 'checked' else 0
        protimeCheckbox = 1 if request.form.get('protimeCheckbox') == 'checked' else 0
        APTTCheckbox = 1 if request.form.get('APTTCheckbox') == 'checked' else 0
        bloodtypingCheckbox = 1 if request.form.get('bloodtypingCheckbox') == 'checked' else 0
        ESRCheckbox = 1 if request.form.get('ESRCheckbox') == 'checked' else 0
        plateCheckbox = 1 if request.form.get('plateCheckbox') == 'checked' else 0
        hgbCheckbox = 1 if request.form.get('hgbCheckbox') == 'checked' else 0
        hctCheckbox = 1 if request.form.get('hctCheckbox') == 'checked' else 0
        cbcCheckbox = 1 if request.form.get('cbcCheckbox') == 'checked' else 0
        reticsCheckbox = 1 if request.form.get('reticsCheckbox') == 'checked' else 0
        CTBTCheckbox = 1 if request.form.get('CTBTCheckbox') == 'checked' else 0

    # BACTERIOLOGY
        culsenCheckbox = 1 if request.form.get('culsenCheckbox') == 'checked' else 0
        cultureCheckbox = 1 if request.form.get('cultureCheckbox') == 'checked' else 0
        gramCheckbox = 1 if request.form.get('gramCheckbox') == 'checked' else 0
        KOHCheckbox = 1 if request.form.get('KOHCheckbox') == 'checked' else 0

    # HISTOPATHOLOGY
        biopsyCheckbox = 1 if request.form.get('biopsyCheckbox') == 'checked' else 0
        papsCheckbox = 1 if request.form.get('papsCheckbox') == 'checked' else 0
        FNABCheckbox = 1 if request.form.get('FNABCheckbox') == 'checked' else 0
        cellCheckbox = 1 if request.form.get('cellCheckbox') == 'checked' else 0
        cytolCheckbox = 1 if request.form.get('cytolCheckbox') == 'checked' else 0

    # CLINICAL MICROSCOPY AND PARASITOLOGY
        urinCheckbox = 1 if request.form.get('urinCheckbox') == 'checked' else 0
        stoolCheckbox = 1 if request.form.get('stoolCheckbox') == 'checked' else 0
        occultCheckbox = 1 if request.form.get('occultCheckbox') == 'checked' else 0
        semenCheckbox = 1 if request.form.get('semenCheckbox') == 'checked' else 0
        ELISACheckbox = 1 if request.form.get('ELISACheckbox') == 'checked' else 0

    # SEROLOGY
        ASOCheckbox = 1 if request.form.get('ASOCheckbox') == 'checked' else 0
        AntiHBSCheckbox = 1 if request.form.get('AntiHBSCheckbox') == 'checked' else 0
        HCVCheckbox = 1 if request.form.get('HCVCheckbox') == 'checked' else 0
        C3Checkbox = 1 if request.form.get('C3Checkbox') == 'checked' else 0
        HIVICheckbox = 1 if request.form.get('HIVICheckbox') == 'checked' else 0
        HIVIICheckbox = 1 if request.form.get('HIVIICheckbox') == 'checked' else 0
        NS1Checkbox = 1 if request.form.get('NS1Checkbox') == 'checked' else 0
        VDRLCheckbox = 1 if request.form.get('VDRLCheckbox') == 'checked' else 0
        PregCheckbox = 1 if request.form.get('PregCheckbox') == 'checked' else 0
        RFCheckbox = 1 if request.form.get('RFCheckbox') == 'checked' else 0
        QuantiCheckbox = 1 if request.form.get('QuantiCheckbox') == 'checked' else 0
        QualiCheckbox = 1 if request.form.get('QualiCheckbox') == 'checked' else 0
        TyphidotCheckbox = 1 if request.form.get('TyphidotCheckbox') == 'checked' else 0
        TubexCheckbox = 1 if request.form.get('TubexCheckbox') == 'checked' else 0
        HAVIgMCheckbox = 1 if request.form.get('HAVIgMCheckbox') == 'checked' else 0
        DengueCheckbox = 1 if request.form.get('DengueCheckbox') == 'checked' else 0

    # IMMUNOCHEMISTRY
        AFPCheckbox = 1 if request.form.get('AFPCheckbox') == 'checked' else 0
        ferritinCheckbox = 1 if request.form.get('ferritinCheckbox') == 'checked' else 0
        HBcIgMCheckbox = 1 if request.form.get('HBcIgMCheckbox') == 'checked' else 0
        AntiHBECheckbox = 1 if request.form.get('AntiHBECheckbox') == 'checked' else 0
        CA125Checkbox = 1 if request.form.get('CA125Checkbox') == 'checked' else 0
        PROBNPCheckbox = 1 if request.form.get('PROBNPCheckbox') == 'checked' else 0
        CA153Checkbox = 1 if request.form.get('CA153Checkbox') == 'checked' else 0
        CA199Checkbox = 1 if request.form.get('CA199Checkbox') == 'checked' else 0
        PSACheckbox = 1 if request.form.get('PSACheckbox') == 'checked' else 0
        CEACheckbox = 1 if request.form.get('CEACheckbox') == 'checked' else 0
        FreeT3Checkbox = 1 if request.form.get('FreeT3Checkbox') == 'checked' else 0
        ANA2Checkbox = 1 if request.form.get('ANA2Checkbox') == 'checked' else 0
        FreeT4Checkbox = 1 if request.form.get('FreeT4Checkbox') == 'checked' else 0
        HBsAGCheckbox = 1 if request.form.get('HBsAGCheckbox') == 'checked' else 0
        TroponiniCheckbox = 1 if request.form.get('TroponiniCheckbox') == 'checked' else 0
        HbACheckbox = 1 if request.form.get('HbACheckbox') == 'checked' else 0
        HBAeAgCheckbox = 1 if request.form.get('HBAeAgCheckbox') == 'checked' else 0
        BetaCheckbox = 1 if request.form.get('BetaCheckbox') == 'checked' else 0
        T3Checkbox = 1 if request.form.get('T3Checkbox') == 'checked' else 0
        T4Checkbox = 1 if request.form.get('T4Checkbox') == 'checked' else 0
        TSHCheckbox = 1 if request.form.get('TSHCheckbox') == 'checked' else 0

    # CLINICAL CHEMISTRY
        ALPCheckbox = 1 if request.form.get('ALPCheckbox') == 'checked' else 0
        AmylaseCheckbox = 1 if request.form.get('AmylaseCheckbox') == 'checked' else 0
        BUACheckbox = 1 if request.form.get('BUACheckbox') == 'checked' else 0
        BUNCheckbox = 1 if request.form.get('BUNCheckbox') == 'checked' else 0
        CreatinineCheckbox = 1 if request.form.get('CreatinineCheckbox') == 'checked' else 0
        SGPTCheckbox = 1 if request.form.get('SGPTCheckbox') == 'checked' else 0
        SGOTCheckbox = 1 if request.form.get('SGOTCheckbox') == 'checked' else 0
        FBSCheckbox = 1 if request.form.get('FBSCheckbox') == 'checked' else 0
        RBSCheckbox = 1 if request.form.get('RBSCheckbox') == 'checked' else 0
        HPPCheckbox = 1 if request.form.get('HPPCheckbox') == 'checked' else 0
        OGCTCheckbox = 1 if request.form.get('OGCTCheckbox') == 'checked' else 0
        HGTCheckbox = 1 if request.form.get('HGTCheckbox') == 'checked' else 0
        OGTTCheckbox = 1 if request.form.get('OGTTCheckbox') == 'checked' else 0
        NaCheckbox = 1 if request.form.get('NaCheckbox') == 'checked' else 0
        MgCheckbox = 1 if request.form.get('MgCheckbox') == 'checked' else 0
        LipidCheckbox = 1 if request.form.get('LipidCheckbox') == 'checked' else 0
        TriglyCheckbox = 1 if request.form.get('TriglyCheckbox') == 'checked' else 0
        CholCheckbox = 1 if request.form.get('CholCheckbox') == 'checked' else 0
        ClCheckbox = 1 if request.form.get('ClCheckbox') == 'checked' else 0
        TPAGCheckbox = 1 if request.form.get('TPAGCheckbox') == 'checked' else 0
        TotalCheckbox = 1 if request.form.get('TotalCheckbox') == 'checked' else 0
        GlobCheckbox = 1 if request.form.get('GlobCheckbox') == 'checked' else 0
        AlbCheckbox = 1 if request.form.get('AlbCheckbox') == 'checked' else 0
        CKMBCheckbox = 1 if request.form.get('CKMBCheckbox') == 'checked' else 0
        CKTotalCheckbox = 1 if request.form.get('CKTotalCheckbox') == 'checked' else 0
        LDHCheckbox = 1 if request.form.get('LDHCheckbox') == 'checked' else 0
        KCheckbox = 1 if request.form.get('KCheckbox') == 'checked' else 0
        CaCheckbox = 1 if request.form.get('CaCheckbox') == 'checked' else 0
        IonizedCheckbox = 1 if request.form.get('IonizedCheckbox') == 'checked' else 0
        PhosCheckbox = 1 if request.form.get('PhosCheckbox') == 'checked' else 0

        result = doctor.add_laboratory_request(patientID=new_patient_id, patientName=patient_fullName, labSubject=lab_subject, gender=sex, age=age, physician=doctorName, orderDate=requestDate, 
                                               otherTest=otherTest, cbcplateCheckbox=cbcplateCheckbox_value, hgbhctCheckbox=hgbhctCheckbox, protimeCheckbox=protimeCheckbox, 
                                               APTTCheckbox=APTTCheckbox, bloodtypingCheckbox=bloodtypingCheckbox, ESRCheckbox=ESRCheckbox, plateCheckbox=plateCheckbox, 
                                               hgbCheckbox=hgbCheckbox, hctCheckbox=hctCheckbox, cbcCheckbox=cbcCheckbox, reticsCheckbox=reticsCheckbox, CTBTCheckbox=CTBTCheckbox, 
                                               culsenCheckbox=culsenCheckbox, cultureCheckbox=cultureCheckbox, gramCheckbox=gramCheckbox, KOHCheckbox=KOHCheckbox, biopsyCheckbox=biopsyCheckbox, 
                                               papsCheckbox=papsCheckbox, FNABCheckbox=FNABCheckbox, cellCheckbox=cellCheckbox, cytolCheckbox=cytolCheckbox, urinCheckbox=urinCheckbox, 
                                               stoolCheckbox=stoolCheckbox, occultCheckbox=occultCheckbox, semenCheckbox=semenCheckbox, ELISACheckbox=ELISACheckbox, ASOCheckbox=ASOCheckbox, 
                                               AntiHBSCheckbox=AntiHBSCheckbox, HCVCheckbox=HCVCheckbox, C3Checkbox=C3Checkbox, HIVICheckbox=HIVICheckbox, HIVIICheckbox=HIVIICheckbox, 
                                               NS1Checkbox=NS1Checkbox, VDRLCheckbox=VDRLCheckbox, PregCheckbox=PregCheckbox, RFCheckbox=RFCheckbox, QuantiCheckbox=QuantiCheckbox, 
                                               QualiCheckbox=QualiCheckbox, TyphidotCheckbox=TyphidotCheckbox, TubexCheckbox=TubexCheckbox, HAVIgMCheckbox=HAVIgMCheckbox, DengueCheckbox=DengueCheckbox, 
                                               AFPCheckbox=AFPCheckbox, ferritinCheckbox=ferritinCheckbox, HBcIgMCheckbox=HBcIgMCheckbox, AntiHBECheckbox=AntiHBECheckbox, CA125Checkbox=CA125Checkbox, 
                                               PROBNPCheckbox=PROBNPCheckbox, CA153Checkbox=CA153Checkbox, CA199Checkbox=CA199Checkbox, PSACheckbox=PSACheckbox, CEACheckbox=CEACheckbox, FreeT3Checkbox=FreeT3Checkbox, 
                                               ANA2Checkbox=ANA2Checkbox, FreeT4Checkbox=FreeT4Checkbox, HBsAGCheckbox=HBsAGCheckbox, TroponiniCheckbox=TroponiniCheckbox, HbACheckbox=HbACheckbox, HBAeAgCheckbox=HBAeAgCheckbox, 
                                               BetaCheckbox=BetaCheckbox, T3Checkbox=T3Checkbox, T4Checkbox=T4Checkbox, TSHCheckbox=TSHCheckbox, ALPCheckbox=ALPCheckbox, AmylaseCheckbox=AmylaseCheckbox, BUACheckbox=BUACheckbox, 
                                               BUNCheckbox=BUNCheckbox, CreatinineCheckbox=CreatinineCheckbox, SGPTCheckbox=SGPTCheckbox, SGOTCheckbox=SGOTCheckbox, FBSCheckbox=FBSCheckbox, RBSCheckbox=RBSCheckbox, 
                                               HPPCheckbox=HPPCheckbox, OGCTCheckbox=OGCTCheckbox, HGTCheckbox=HGTCheckbox, OGTTCheckbox=OGTTCheckbox, NaCheckbox=NaCheckbox, MgCheckbox=MgCheckbox, LipidCheckbox=LipidCheckbox, 
                                               TriglyCheckbox=TriglyCheckbox, CholCheckbox=CholCheckbox, ClCheckbox=ClCheckbox, TPAGCheckbox=TPAGCheckbox, TotalCheckbox=TotalCheckbox, GlobCheckbox=GlobCheckbox, AlbCheckbox=AlbCheckbox, 
                                               CKMBCheckbox=CKMBCheckbox, CKTotalCheckbox=CKTotalCheckbox, LDHCheckbox=LDHCheckbox, KCheckbox=KCheckbox, CaCheckbox=CaCheckbox, IonizedCheckbox=IonizedCheckbox, PhosCheckbox=PhosCheckbox) 

        new_lab_results = doctor.get_patient_info(new_patient_id)
        print('result', result)

        if result:
            return render_template("doctor/patient/labtest_request.html", success=True, doctor=doctor_info, PatientForm=form, patient_id=patient_id, patient=new_lab_results)
        else:
            return render_template("doctor/patient/labtest_request.html", error=True, doctor=doctor_info, PatientForm=form, patient_id=patient_id, patient=new_lab_results)

    return render_template("doctor/patient/labtest_request.html", patient_id=patient_id, Patientform=form)

# PRESCRIPTION
@doctor_bp.route('/prescription/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def prescription():
    form = PatientForm()
    patient_id = None

    if request.method == 'GET':
        user_id = current_user.id
        patient_id = request.args.get('patient_id')
        assessment_id = request.args.get('assessment_id')
        patient_info = doctor.get_patient_info(patient_id)
        consultation_info = doctor.get_consultation_info(assessment_id, patient_id)
        prescription_info = doctor.get_prescription_info(assessment_id)
        doctor_info = doctor.get_doctor_info(user_id)

        return render_template('doctor/patient/prescription.html', doctor=doctor_info, patient=patient_info, consultation=consultation_info, prescriptions=prescription_info, patient_id=patient_id, PatientForm=form)
    
    elif request.method == 'POST':
        prescription_data = request.get_json()
        new_assessment_id = prescription_data.get('assessment_id')
        new_patient_id = prescription_data.get('patient_id')
        prescriptions = prescription_data.get('prescriptions')
    
        for prescription in prescriptions:
            medication_name = prescription['medicationName'].capitalize()
            dosage = prescription['dosage'].upper()
            p_quantity = prescription['quantity'].capitalize()
            duration = prescription['duration'].capitalize()
            instructions = prescription['instructions'].capitalize()

            result = doctor.add_prescription(assessment_id=new_assessment_id, medication_name=medication_name, dosage=dosage, p_quantity=p_quantity, duration=duration, instructions=instructions)
        
        patient_info = doctor.get_patient_info(new_patient_id)
        consultation_info = doctor.get_consultation_info(new_assessment_id, new_patient_id)
        prescription_info = doctor.get_prescription_info(new_assessment_id)
        print('new prescription INFORMATION:', prescription_info)
        print('RESULT:', result)

        if result:
            return jsonify({'success': True})
        else:
             return jsonify({'error': True}), 500  

    return render_template("doctor/patient/prescription.html", consultation=consultation_info, patient=patient_info, prescriptions=prescription_info, patient_id=patient_id, PatientForm=form)

# DELETE PATIENT RECORD
@doctor_bp.route('/delete_patient/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def delete_patient():
    form = PatientForm()

    if request.method == "POST":
        patient_id = request.form.get("patient_id")

        result = doctor.delete_patient_record(patient_id)

        if result:
            return render_template("doctor/patient/patient.html", success=True, PatientForm=form)
        else:
            return render_template("doctor/patient/patient.html", error=True, PatientForm=form)
        
    return render_template("doctor/patient/patient.html", PatientForm=form)

# DELETE ASSESSMENT RECORD
@doctor_bp.route('/delete_assessment/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def delete_assessment():
    form = PatientForm()

    if request.method == "POST":
        assessment_id = request.form.get("assessment_id")
        patient_id = request.form.get("patient_id")

        result = doctor.delete_medical_assessment(assessment_id, patient_id)
        patient_info = doctor.get_patient_info(patient_id)

        if result:
            return render_template("doctor/patient/consultation.html", success=True, patient=patient_info, PatientForm=form)
        else:
            return render_template("doctor/patient/consultation.html", error=True, patient=patient_info, PatientForm=form)
        
    return render_template("doctor/patient/consultation.html", PatientForm=form)


# APPOINTMENT ROUTES
def generate_reference_number():
    characters = string.ascii_uppercase + string.digits
    reference_number = ''.join(secrets.choice(characters) for _ in range(6))
    return reference_number

def generate_status():
    return 'PENDING'

def generate_cancel_status():
    return 'CANCELLED'

@doctor_bp.route('/add-appointment/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def add_appointment():
    form = AppointmentForm(request.form)
    user_id = current_user.id
    print("User ID:", user_id)
    booking_details = None
    time_schedules = None
    doctor_id = None
    doctor_names = Appointment.get_all_doctor_name(user_id)
    receptionist_ids = Appointment.get_receptionist_id()

    if request.method == 'POST':
        print(request.form)  # Print form data
        print(request.files)  # Print file uploads
        try:
            check_reference = generate_reference_number()
            print('Reference: ', check_reference)
            form.reference_number.data = check_reference 
            initial_status = generate_status()
            form.status_.data = initial_status

            # Extract the chosen doctor from the form data
            chosen_doctor = request.form['doctorName']
            print('Before print statements. Chosen doctor:', chosen_doctor)
            doctor_id_dict = Appointment.get_doctor_id(chosen_doctor)

            # Extract the ID from the dictionary
            doctor_id = doctor_id_dict['id']
            print('In the add route, doctor ID is:', doctor_id)
            print('After print statements.')
            
            # Extract the chosen date from the form data
            chosen_date = request.form['date_appointment']
            form.date_appointment.data = chosen_date  # Set the form field with the chosen date

            # Fetch available time schedules for the chosen date
            time_schedules = Appointment.all_time_schedules(chosen_date, chosen_doctor)
            
            # Get the selected time from the form
            selected_time = request.form['time_appointment']

            # Update the slots in the schedule table
            Appointment.update_slots(chosen_date, selected_time, chosen_doctor, increment=False)
            print(request.form)  # Print the form data for debugging

            if form.validate_on_submit():
                reference_exists = Appointment.unique_code(check_reference)
                
                if reference_exists:
                    flash("Appointment already exists. Please enter a new appointment.")
                else:
                    new_appointment = Appointment(
                        reference_number=form.reference_number.data,
                        receptionistID=form.receptionistID.data,
                        doctorID=form.doctorID.data,
                        doctorName=form.doctorName.data,
                        date_appointment=form.date_appointment.data,
                        time_appointment=form.time_appointment.data,
                        status_=form.status_.data,
                        first_name=form.first_name.data,
                        middle_name=form.middle_name.data,
                        last_name=form.last_name.data,
                        sex=form.sex.data,
                        birth_date=form.birth_date.data,
                        contact_number=form.contact_number.data,
                        email=form.email.data,
                        address=form.address.data
                    )
                    new_appointment.add()
                    flash('New appointment added!', 'success')
                    
                    # Fetch booking details after adding the appointment
                    booking_details = Appointment.get_booking_reference_details(form.reference_number.data)
                    
                    print(booking_details)
                    
                    return jsonify(success=True, message="Appointment added successfully", booking_details=booking_details)
            else:
                print(form.errors)  # Add this line to print form errors for debugging
                flash('Failed to add appointment. Please check the form for errors.', 'danger')
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            flash('An error occurred while processing the appointment.', 'danger')
            # Set time_schedules to an empty list in case of an error
            time_schedules = []
            return jsonify(success=False, message="Internal Server Error"), 500

    return render_template("doctor/appointment/appointment_add_v2.html", form=form, booking_details=booking_details, time_schedules=time_schedules, doctor_names=doctor_names, doctor_id=doctor_id, receptionist_ids=receptionist_ids)


@doctor_bp.route('/delete-appointment/', methods=['POST'])
@login_required
@role_required('doctor')
def delete_appointment():
    try:
        reference_number = request.form.get('reference_number')
        doctor_name = request.form.get('doctor_name')
        print('Doctor Name: ', doctor_name)
        
        # Retrieve the time of the deleted appointment
        deleted_appointment = Appointment.get_appointment_by_reference(reference_number)
        deleted_time = deleted_appointment['time_appointment']

        if Appointment.delete(reference_number):
            # Increment the slots for the deleted time
            Appointment.update_slots(deleted_appointment['date_appointment'], deleted_time, doctor_name, increment=True)
            
            return jsonify(success=True, message="Successfully deleted")
        else:
            return jsonify(success=False, message="Failed to delete appointment")
    except Exception as e:
        # Log the error for debugging purposes
        doctor_bp.logger.error("An error occurred: %s" % str(e))
        return jsonify(success=False, message="Internal Server Error"), 500

@doctor_bp.route('/view-appointment/', methods=["GET"])
@login_required
@role_required('doctor')
def view_appointment():
    booking_ref_number = request.args.get('reference_number')
    view_appointment = Appointment.view_appointment_by_reference(booking_ref_number)
    print(view_appointment)
    
    if view_appointment:
        appointment_data_dict = {
            "reference_number": view_appointment['reference_number'],
            "date_appointment": view_appointment['date_appointment'],
            "time_appointment": view_appointment['time_appointment'],
            "book_date": view_appointment['book_date'],
            "status_": view_appointment['status_'],
            "appointment_first_name": view_appointment['appointment_first_name'],
            "appointment_middle_name": view_appointment['appointment_middle_name'],
            "appointment_last_name": view_appointment['appointment_last_name'],
            "sex": view_appointment['sex'],
            "birth_date": view_appointment['birth_date'],
            "contact_number": view_appointment['contact_number'],
            "email": view_appointment['email'],
            "address": view_appointment['address'],
            "user_first_name": view_appointment['user_first_name'],
            "user_middle_name": view_appointment['user_middle_name'],
            "user_last_name": view_appointment['user_last_name']
        }
        print(appointment_data_dict)
    else:
        flash("Appointment not found.", "error")
        return jsonify(success=False, message="Appointment not found.")
    
    return render_template("doctor/appointment/appointment_view.html", row=appointment_data_dict)


@doctor_bp.route('/get-booking-details/<reference_number>', methods=['GET'])
@login_required
@role_required('doctor')
def get_booking_details(reference_number):
    booking_details = Appointment.get_booking_reference_details(reference_number)

    if booking_details:
        return jsonify(booking_details)
    else:
        return jsonify({'error': 'Booking details not available'}), 404


@doctor_bp.route('/edit-appointment-version-two/', methods=["GET", "POST"])
@login_required
@role_required('doctor')
def reschedule_version_two():
    reference_number = request.form.get('reference_number')
    doctor_name = request.form.get('doctor_name')
    print('Reference number inside reschedule', reference_number)
    print('Doctor name inside reschedule', doctor_name)
    form = EditAppointmentForm()
    appointment_data = Appointment.get_appointment_by_reference_version_two(reference_number)

    if appointment_data:
        appointment_data_dict = {
            "reference_number": appointment_data['reference_number'],
            "date_appointment": appointment_data['date_appointment'],
            "time_appointment": appointment_data['time_appointment'],
            "status_": appointment_data['status_'],
            "last_name": appointment_data['last_name'],
            "email": appointment_data['email'],
            "doctorName": appointment_data['doctorName']
        }
        time_data = Appointment.get_all_available_schedules(appointment_data['date_appointment'])
        print(appointment_data_dict)
        print(time_data)
    else:
        return jsonify(success=False, message="Appointment not found.")

    if request.method == "POST" and form.validate():
        new_date_appointment = form.date_appointment.data
        new_time_appointment = form.time_appointment.data
        new_status_ = form.status_.data
        new_last_name = form.last_name.data
        new_email = form.email.data

        old_date_appointment = appointment_data['date_appointment']
        old_time_appointment = appointment_data['time_appointment']
        print('Old Appointment Details: ', old_date_appointment, old_time_appointment)
        print('New Appointment Details: ', new_date_appointment, new_time_appointment)
        if Appointment.update_second_version(
            reference_number, new_date_appointment, new_time_appointment, new_status_,
            new_last_name, new_email):
            # Update the slots for the old and new times
            Appointment.update_time_slots(old_date_appointment, new_date_appointment, old_time_appointment, new_time_appointment, doctor_name)

            return jsonify(success=True, message="Appointment updated successfully")
        else:
            return jsonify(success=False, message="Failed to update appointment.")
    else:
        print ("Failed to update appointment")
        print("Form validation failed:", form.errors)
    return render_template("doctor/appointment/appointment.html", form=form, data=appointment_data_dict, time_data=time_data)


@doctor_bp.route('/search-appointments/', methods=['POST'])
@login_required
@role_required('doctor')
def search_appointments():
    try:
        user_id = current_user.id
        data = request.get_json()
        print("Received data:", data) 
        search_query = data.get('searchTerm')
        print("Search term:", search_query)
        filter_by = data.get('filterBy')
        print("Filter by:", filter_by)
        
        if filter_by == 'all':
            search_results = Appointment.search_appointment(search_query, user_id)
            print("Search results:", search_results)
        else:
            search_results = Appointment.filter_appointment(filter_by, search_query, user_id)
            print("Search results:", search_results)
            
        return jsonify({'success': True, 'data': search_results})
    except Exception as e:
        print("Error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

    
@doctor_bp.route('/get-time-schedules', methods=['POST'])
@login_required
@role_required('doctor')
def get_time_schedules():
    try:
        selected_date = request.form['selected_date']
        selected_doctor = request.form['selected_doctor']  # Add this line to get the selected doctor
        print("Selected doctor in time:", selected_doctor)
        time_schedules = Appointment.all_time_schedules(selected_date, selected_doctor)
        return jsonify(success=True, time_schedules=time_schedules)
    except Exception as e:
        return jsonify(success=False, message=str(e))

@doctor_bp.route('/cancel-appointment/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def cancel_appointment():
    try:
        reference_number = request.form.get('reference_number')
        doctor_name = request.form.get('doctor_name')
        print('Name in cancel: ', doctor_name)
        cancel_status = generate_cancel_status()
        
        # Retrieve the time of the deleted appointment
        cancel_appointment = Appointment.get_appointment_by_reference(reference_number)
        cancelled_time = cancel_appointment['time_appointment']

        if Appointment.update_to_cancel(reference_number, cancel_status):
            # Increment the slots for the deleted time
            Appointment.update_slots(cancel_appointment['date_appointment'], cancelled_time, doctor_name, increment=True)

            return jsonify(success=True, message="Successfully cancelled the appointment")
        else:
            return jsonify(success=False, message="Failed to cancel appointment")
    except Exception as e:
        # Log the error for debugging purposes
        doctor_bp.logger.error("An error occurred: %s" % str(e))
        return jsonify(success=False, message="Internal Server Error"), 500

@doctor_bp.route('/get-appointment-data/', methods=['GET'])
@login_required
@role_required('doctor')
def get_appointment_data():
    try:
        reference_number = request.args.get('referenceNumber')

        # Ensure the reference number is provided
        if not reference_number:
            return jsonify(success=False, message="Reference number is required.")

        # Fetch appointment data using the provided reference number
        appointment_data = Appointment.get_appointment_by_reference_version_two(reference_number)

        if appointment_data:
            # Fetch time options based on the appointment's date
            date_appointment = appointment_data.get('date_appointment')  # Adjust accordingly
            time_options = Appointment.get_all_available_schedules(date_appointment)

            return jsonify(success=True, appointmentData=appointment_data, timeOptions=time_options)
        else:
            return jsonify(success=False, message="Appointment not found.")

    except Exception as e:
        print("Error:", str(e))
        return jsonify(success=False, message="An error occurred.")
    
    
@doctor_bp.route('/get-doctor-id/', methods=['POST'])
@login_required
@role_required('doctor')
def get_doctor_id():
    try:
        selected_doctor = request.form['doctorName']
        print('Selected doctor:', selected_doctor)
        doctor_id = Appointment.get_doctor_id(selected_doctor)
        print('Doctor ID', doctor_id)
        return jsonify(success=True, doctor_id=doctor_id)
    except Exception as e:
        return jsonify(success=False, message=str(e))