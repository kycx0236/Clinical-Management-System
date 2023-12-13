from flask import render_template, request, jsonify, redirect, url_for
from app.forms.doctor_f import *
import app.models as models
from app.models.doctor_m import *
from flask import Blueprint
from flask_login import login_required, logout_user, current_user
from app.routes.utils import role_required

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/')
@login_required
@role_required('doctor')
def dashboard():
    current_id = current_user.id 
    doctor_info = doctor.get_doctor_info(current_id)
    patients_data = doctor.get_patients(current_id)
    limited_patient = patients_data[:5]

    return render_template("doctor/dashboard/dashboard.html", info=doctor_info, patients=limited_patient)

@doctor_bp.route('/calendar/')
@login_required
@role_required('doctor')
def calendar():
    current_id = current_user.id 
    doctor_info = doctor.get_doctor_info(current_id)
    return render_template("doctor/calendar/calendar.html", info=doctor_info)

@doctor_bp.route('/appointment/')
@login_required
@role_required('doctor')
def appointment():
    current_id = current_user.id 
    doctor_info = doctor.get_doctor_info(current_id)
    return render_template("doctor/appointment/appointment.html", info=doctor_info)

@doctor_bp.route('/schedule/')
@login_required
@role_required('doctor')
def schedule():
    current_id = current_user.id 
    doctor_info = doctor.get_doctor_info(current_id)
    return render_template("doctor/schedule/schedule.html", info=doctor_info)

@doctor_bp.route('/profile/')
@login_required
@role_required('doctor')
def profile():
    current_id = current_user.id 
    doctor_info = doctor.get_doctor_info(current_id)
    return render_template("doctor/profile/profile.html", info=doctor_info)

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
    doctor_info = doctor.get_doctor_info(user_id)

    if request.method == 'POST':
        doctor_info = doctor.get_doctor_info(user_id)
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
        job = form.occupation.data.upper()
        emailAdd = form.email.data
        p_num = form.contact_num.data
        cAddress = form.p_address.data.upper()
        p_nationality = form.nationality.data
        e_person = form.e_person.data.upper()
        relationship = form.relationship.data
        e_number = form.e_number.data
        
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
        new_patient.userID = user_id

        result = new_patient.add(user_id)

        if result:
            return render_template("doctor/patient/add_patient.html", success=True, PatientForm=form, info=doctor_info)
        else:
            return render_template("doctor/patient/add_patient.html", error=True, PatientForm=form, info=doctor_info)

    return render_template("doctor/patient/add_patient.html", PatientForm=form, info=doctor_info)

# ADD AND UPDATE MEDICAL HISTORY
@doctor_bp.route('/medical_history/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def medical_history():
    form = PatientForm()
    patient_id = None
    user_id = current_user.id
    
    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        patient_info = doctor.get_patient_history (patient_id)
        doctor_info = doctor.get_doctor_info(user_id)

        return render_template('doctor/patient/medical_history.html', patient=patient_info, PatientForm=form, patient_id=patient_id, info=doctor_info)

    elif request.method == 'POST':
        new_history_id = request.form.get('history_id')
        new_patient_id = request.form.get('patient_id')
        doctor_info = doctor.get_doctor_info(user_id)

    # IMMUNIZATION
        bcg_checkbox_value = form.bcgCheckbox.data
        dtp_checkbox_value = form.dtpCheckbox.data
        pcv_checkbox_value = form.pcvCheckbox.data
        influenza_checkbox_value = form.influenzaCheckbox.data
        hepa_checkbox_value = form.hepaCheckbox.data
        ipv_checkbox_value = form.ipvCheckbox.data
        mmr_checkbox_value = form.mmrCheckbox.data
        hpv_checkbox_value = form.hpvCheckbox.data

    # FAMILY HISTORY
        asthma_checkbox_value = form.asthmaCheckbox.data
        diabetes_checkbox_value = form.diabetesCheckbox.data
        heart_checkbox_value = form.heartCheckbox.data
        birth_checkbox_value = form.birthCheckbox.data
        bone_checkbox_value = form.boneCheckbox.data
        alzheimer_checkbox_value = form.alzheimerCheckbox.data
        cancer_checkbox_value = form.cancerCheckbox.data
        thyroid_checkbox_value = form.thyroidCheckbox.data
        tuberculosis_checkbox_value = form.tuberculosisCheckbox.data
        eye_checkbox_value = form.eyeCheckbox.data
        clots_checkbox_value = form.clotsCheckbox.data
        mental_checkbox_value = form.mentalCheckbox.data
        kidney_checkbox_value = form.kidneyCheckbox.data
        anemia_checkbox_value = form.anemiaCheckbox.data
        muscle_checkbox_value = form.muscleCheckbox.data
        highblood_checkbox_value = form.highbloodCheckbox.data
        epilepsy_checkbox_value = form.epilepsyCheckbox.data
        skin_checkbox_value = form.skinCheckbox.data
        hiv_checkbox_value = form.hivCheckbox.data
        pulmonary_checkbox_value = form.pulmonaryCheckbox.data
        new_specifications = form.specifications.data.upper()
        new_others = form.others.data.upper()

    # PAST HISTORY
        new_past1 = form.past_c1.data.upper()
        new_medication1 = form.medication1.data.upper()
        new_dosage1 = form.dosage1.data.upper()
        new_hdate1 = form.h_date1.data
        if not new_hdate1:
            new_hdate1 = None 
        new_past2 = form.past_c2.data.upper()
        new_medication2 = form.medication2.data.upper()
        new_dosage2 = form.dosage2.data.upper()
        new_hdate2 = form.h_date2.data
        if not new_hdate2:
            new_hdate2 = None
        new_past3 = form.past_c3.data.upper()
        new_medication3 = form.medication3.data.upper()
        new_dosage3 = form.dosage3.data.upper()
        new_hdate3 = form.h_date3.data
        if not new_hdate3:
            new_hdate3 = None

    # SOCIAL HISTORY 
        habit = form.habitually.data
        yDrunk = form.yearsDrunk.data
        fDrink = form.frequencyDrink.data.upper()
        qDrink = form.quitDrinking.data
        frequent = form.frequently.data
        ySmoked = form.yearsSmoked.data
        fSmoke = form.frequencySmoke.data.upper()
        qSmoke = form.quitSmoking.data
        often = form.often.data
        eType = form.exerciseType.data.upper()
        fExercise = form.frequencyExercise.data.upper()
        dActivity = form.durationActivity.data.upper()
        sActive = form.sexActive.data
        sPartner = form.sexPartner.data
        nSPartner = form.numSexPartner.data
        contraceptions = form.contraception.data.upper()
        use = form.useDrugs.data
        sDrugs = form.specifyDrugs.data.upper()
        fDrugs = form.frequencyDrugs.data.upper()
        diet = form.diet.data.upper()

    # SURGICAL HISTORY  
        sDate1 = form.surgeryDate1.data
        sProcedure1 = form.surgeryProcedure1.data.upper()
        shospital1 = form.hospital1.data.upper()
        sDate2 = form.surgeryDate2.data
        sProcedure2 = form.surgeryProcedure2.data.upper()
        shospital2 = form.hospital2.data.upper()
        sDate3 = form.surgeryDate3.data
        sProcedure3 = form.surgeryProcedure3.data.upper()
        shospital3 = form.hospital3.data.upper()

    # MEDICATIONS
        meds = form.medications.data.upper()

    # ALLERGIES
        allergy = form.allergies.data.upper()

        existing_history = doctor.get_patient_history(new_patient_id)
        
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
            
            if updated:
                return render_template("doctor/patient/medical_history.html", new_patient_id=new_patient_id, success=True, patient=updated_info, PatientForm=form, info=doctor_info)
            else:
                return render_template("doctor/patient/medical_history.html", new_patient_id=new_patient_id, error=True, patient=updated_info, PatientForm=form, info=doctor_info)

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

            if result:
                return render_template("doctor/patient/medical_history.html", patient_id=patient_id, success=True, patient=updated_info, PatientForm=form, info=doctor_info)
            else:
                return render_template("doctor/patient/medical_history.html", patient_id=patient_id, error=True, patient=updated_info, PatientForm=form, info=doctor_info)

    return render_template("doctor/patient/medical_history.html", patient_id=patient_id, PatientForm=form, info=doctor_info)

# ADD MEDICAL CLEARANCE FOR EACH APPOINTMENT
@doctor_bp.route('/add_clearance/')
@login_required
@role_required('doctor')
def add_clearance():
    current_id = current_user.id 
    doctor_info = doctor.get_doctor_info(current_id)
    patient_id = request.args.get('patient_id')

    return render_template("doctor/patient/add_clearance.html", patient_id=patient_id, info=doctor_info)

# ADD MEDICAL CERTIFICATE FOR EACH APPOINTMENT
@doctor_bp.route('/add_certificate/')
@login_required
@role_required('doctor')
def add_certificate():
    form = PatientForm()
    current_id = current_user.id 
    doctor_info = doctor.get_doctor_info(current_id)
    patient_id = request.args.get('patient_id')

    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        assessment_id = request.args.get('assessment_id')
        patient_info = doctor.get_patient_info(patient_id)
        consultation_info = doctor.get_consultation_info(assessment_id, patient_id)
        doctor_info = doctor.get_doctor_info(current_id)

        return render_template('doctor/patient/add_certificate.html', info=doctor_info, patient=patient_info, consultation=consultation_info, patient_id=patient_id, PatientForm=form)

    return render_template("doctor/patient/add_certificate.html", patient_id=patient_id, info=doctor_info)

# ADD MEDICAL ASSESSMENT FOR EACH APPOINTMENT
@doctor_bp.route('/add_assessment/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def add_assessment():
    form = PatientForm()
    patient_id = None
    user_id = current_user.id

    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        patient_info = doctor.get_patient_info(patient_id)
        doctor_info = doctor.get_doctor_info(user_id)

        return render_template('doctor/patient/add_assessment.html', patient=patient_info, PatientForm=form, patient_id=patient_id, info=doctor_info)
    
    elif request.method == 'POST':
        new_patient_id = request.form.get('patient_id')
        doctor_info = doctor.get_doctor_info(user_id)

    # COMPLAINT
        sub = form.subject.data.upper()
        complain = form.complaints.data.upper()

    # HISTORY OF PRESENT ILLNESS
        p_illness = form.h_illness.data.upper()

    # VITAL SIGNS
        blood_p = form.blood_p.data.upper()
        pulse_r = form.pulse_r.data.upper()
        temp = form.temp.data.upper()
        respiratory_r = form.respiratory_r.data.upper()
        height = form.height.data
        weight = form.weight.data
        body_mass = form.body_mass.data
        oxygenSaturation = form.oxygenSaturation.data.upper()
        painSection = form.painSection.data.upper()

    # PHYSICAL EXAMINATIONS
        normal_head = form.normal_head.data.upper()
        abnormalities_head = form.abnormalities_head.data.upper()
        normal_ears = form.normal_ears.data.upper()
        abnormalities_ears = form.abnormalities_ears.data.upper()
        normal_eyes = form.normal_eyes.data.upper()
        abnormalities_eyes = form.abnormalities_eyes.data.upper()
        normal_nose = form.normal_nose.data.upper()
        abnormalities_nose = form.abnormalities_nose.data.upper()
        normal_skin = form.normal_skin.data.upper()
        abnormalities_skin = form.abnormalities_skin.data.upper()
        normal_back = form.normal_back.data.upper()
        abnormalities_back = form.abnormalities_back.data.upper()
        normal_neck = form.normal_neck.data.upper()
        abnormalities_neck = form.abnormalities_neck.data.upper()
        normal_throat = form.normal_throat.data.upper()
        abnormalities_throat = form.abnormalities_throat.data.upper()
        normal_chest = form.normal_chest.data.upper()
        abnormalities_chest = form.abnormalities_chest.data.upper()
        normal_abdomen = form.normal_abdomen.data.upper()
        abnormalities_abdomen = form.abnormalities_abdomen.data.upper()
        normal_upper = form.normal_upper.data.upper()
        abnormalities_upper = form.abnormalities_upper.data.upper()
        normal_lower = form.normal_lower.data.upper()
        abnormalities_lower = form.abnormalities_lower.data.upper()
        normal_tract = form.normal_tract.data.upper()
        abnormalities_tract = form.abnormalities_tract.data.upper()
        comments = form.comments.data.upper()

    # DIAGNOSIS
        diagnosis = form.diagnosis.data.upper()

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
            return render_template("doctor/patient/add_assessment.html", patient_id=patient_id, success=True, patient=new_consultation, PatientForm=form, info=doctor_info)
        else:
            return render_template("doctor/patient/add_assessment.html", patient_id=patient_id, error=True, patient=new_consultation, PatientForm=form, info=doctor_info)

    return render_template("doctor/patient/add_assessment.html", patient_id=patient_id, PatientForm=form, info=doctor_info)

# PATIENT TABLE
@doctor_bp.route('/patient/')
@login_required
@role_required('doctor')
def patient():
    user_id = current_user.id
    doctor_info = doctor.get_doctor_info(user_id)
    patients_data = doctor.get_patients(user_id)

    return render_template("doctor/patient/patient.html", patients=patients_data, info=doctor_info)

# CONSULTATION TABLE
@doctor_bp.route('/consultation/')
@login_required
@role_required('doctor')
def consultation():
    patient_id = request.args.get('patient_id')
    patient_info = doctor.get_patient_info(patient_id)
    consultation_data = doctor.get_consultations(patient_id)
    user_id = current_user.id
    doctor_info = doctor.get_doctor_info(user_id)

    return render_template("doctor/patient/consultation.html", consultations=consultation_data,patient=patient_info, patient_id=patient_id, info=doctor_info)

# LAB RESULTS TABLE
@doctor_bp.route('/lab_results/')
@login_required
@role_required('doctor')
def lab_results():
    patient_id = request.args.get('patient_id')
    report_info = doctor.get_lab_reports(patient_id)
    user_id = current_user.id
    doctor_info = doctor.get_doctor_info(user_id)

    return render_template("doctor/patient/lab_results.html", patient_id=patient_id, labreports=report_info, info=doctor_info)

# UPDATE PATIENT INFORMATION
@doctor_bp.route('/patient_record/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def patient_record():
    form = PatientForm()
    user_id = current_user.id

    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        patient_info = doctor.get_patient_info(patient_id)
        doctor_info = doctor.get_doctor_info(user_id)

        return render_template('doctor/patient/patient_record.html', patient=patient_info, patient_id=patient_id, PatientForm=form, info=doctor_info)

    elif request.method == 'POST':
        doctor_info = doctor.get_doctor_info(user_id)
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

        updated = doctor.update_patient_info(patientID=new_patient_id, firstName=new_first_name, midName=new_middle_name, lastName=new_last_name, age=new_age, 
                                             civilStatus=new_civil_status, gender=new_gender, bloodType=new_bloodType, religion=new_religion, birthPlace=new_birth_place, 
                                             occupation=new_occupation, p_email=new_email, p_contactNum=new_contact_num, birthDate=new_birth_date, p_address=new_p_address, 
                                             nationality=new_nationality, eContactName=new_e_person, relationship=new_relationship, eContactNum=new_e_number)  
        
        print('New Patient ID:', new_patient_id)

        updated_info = doctor.get_patient_info(new_patient_id)
        print('Updated information:', updated_info)

        if updated:
            return render_template("doctor/patient/patient_record.html", new_patient_id=new_patient_id, success=True, patient=updated_info, PatientForm=form, info=doctor_info)
        else:
            return render_template("doctor/patient/patient_record.html", new_patient_id=new_patient_id, error=True, patient=updated_info, PatientForm=form, info=doctor_info)

    return render_template("doctor/patient/patient_record.html", PatientForm=form, info=doctor_info)


# UPDATE MEDICAL ASSESSMENT
@doctor_bp.route('/assessment/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def assessment():
    form=PatientForm()
    patient_id = None
    user_id = current_user.id

    if request.method == 'GET':
        doctor_info = doctor.get_doctor_info(user_id)
        assessment_id = request.args.get('assessment_id')
        patient_id = request.args.get('patient_id')
        patient_info = doctor.get_consultation_info(assessment_id, patient_id)
        
        return render_template('doctor/patient/assessment.html', patient=patient_info, PatientForm=form, patient_id=patient_id, info=doctor_info)
    
    elif request.method == 'POST':
        doctor_info = doctor.get_doctor_info(user_id)
        new_assessment_id = request.form.get('assessment_id')
        new_patient_id = request.form.get('patient_id')
        
    # COMPLAINT
        sub = form.subject.data.upper()
        complain = form.complaints.data.upper()

    # HISTORY OF PRESENT ILLNESS
        p_illness = form.h_illness.data.upper()

    # VITAL SIGNS
        blood_p = form.blood_p.data.upper()
        pulse_r = form.pulse_r.data.upper()
        temp = form.temp.data.upper()
        respiratory_r = form.respiratory_r.data.upper()
        height = form.height.data
        weight = form.weight.data
        body_mass = form.body_mass.data
        oxygenSaturation = form.oxygenSaturation.data.upper()
        painSection = form.painSection.data.upper()

    # PHYSICAL EXAMINATIONS
        normal_head = form.normal_head.data.upper()
        abnormalities_head = form.abnormalities_head.data.upper()
        normal_ears = form.normal_ears.data.upper()
        abnormalities_ears = form.abnormalities_ears.data.upper()
        normal_eyes = form.normal_eyes.data.upper()
        abnormalities_eyes = form.abnormalities_eyes.data.upper()
        normal_nose = form.normal_nose.data.upper()
        abnormalities_nose = form.abnormalities_nose.data.upper()
        normal_skin = form.normal_skin.data.upper()
        abnormalities_skin = form.abnormalities_skin.data.upper()
        normal_back = form.normal_back.data.upper()
        abnormalities_back = form.abnormalities_back.data.upper()
        normal_neck = form.normal_neck.data.upper()
        abnormalities_neck = form.abnormalities_neck.data.upper()
        normal_throat = form.normal_throat.data.upper()
        abnormalities_throat = form.abnormalities_throat.data.upper()
        normal_chest = form.normal_chest.data.upper()
        abnormalities_chest = form.abnormalities_chest.data.upper()
        normal_abdomen = form.normal_abdomen.data.upper()
        abnormalities_abdomen = form.abnormalities_abdomen.data.upper()
        normal_upper = form.normal_upper.data.upper()
        abnormalities_upper = form.abnormalities_upper.data.upper()
        normal_lower = form.normal_lower.data.upper()
        abnormalities_lower = form.abnormalities_lower.data.upper()
        normal_tract = form.normal_tract.data.upper()
        abnormalities_tract = form.abnormalities_tract.data.upper()
        comments = form.comments.data.upper()

    # DIAGNOSIS
        diagnosis = form.diagnosis.data.upper()

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
            return render_template("doctor/patient/assessment.html", new_patient_id=new_patient_id, success=True, patient=new_consultation, PatientForm=form, info=doctor_info)
        else:
            return render_template("doctor/patient/assessment.html", new_patient_id=new_patient_id, error=True, patient=new_consultation, PatientForm=form, info=doctor_info)

    return render_template("doctor/patient/assessment.html", patient_id=patient_id, PatientForm=form, info=doctor_info)
  
# LABORATORY RESULT
@doctor_bp.route('/results/')
@login_required
@role_required('doctor')
def results():
    form=PatientForm()
    patient_id = None
    user_id = current_user.id
    doctor_info = doctor.get_doctor_info(user_id)

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
                               immunochem=immunochem_info, clinicalchem=clinicalchem_info, reports=lab_report, report=labrep_info, info=doctor_info)

# REQUEST TO RUN LABORATORY TESTS
@doctor_bp.route('/labtest_request/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def labtest_request():
    form=PatientForm()
    patient_id = None
    user_id = current_user.id

    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        patient_info = doctor.get_patient_info(patient_id)
        doctor_info = doctor.get_doctor_info(user_id)

        return render_template('doctor/patient/labtest_request.html', patient=patient_info, doctor=doctor_info, PatientForm=form, patient_id=patient_id)
    
    elif request.method == 'POST':
        doctor_info = doctor.get_doctor_info(user_id)
        new_patient_id = request.form.get('patient_id')

    # PATIENT INFORMATION
        patient_fullName = form.fullName.data
        lab_subject = form.labsubject.data.upper()
        sex = form.gender.data
        age = form.age.data
        doctorName = form.doctorName.data
        requestDate = form.dateofRequest.data
        otherTest = form.others.data.upper()

    # HEMATOLOGY
        cbcplateCheckbox_value = form.cbcplateCheckbox.data
        hgbhctCheckbox = form.hgbhctCheckbox.data
        protimeCheckbox = form.protimeCheckbox.data
        APTTCheckbox = form.APTTCheckbox.data
        bloodtypingCheckbox = form.bloodtypingCheckbox.data
        ESRCheckbox = form.ESRCheckbox.data
        plateCheckbox = form.plateCheckbox.data
        hgbCheckbox = form.hgbCheckbox.data
        hctCheckbox = form.hctCheckbox.data
        cbcCheckbox = form.cbcCheckbox.data
        reticsCheckbox = form.reticsCheckbox.data
        CTBTCheckbox = form.CTBTCheckbox.data

    # BACTERIOLOGY
        culsenCheckbox = form.culsenCheckbox.data
        cultureCheckbox = form.cultureCheckbox.data
        gramCheckbox = form.gramCheckbox.data
        KOHCheckbox = form.KOHCheckbox.data

    # HISTOPATHOLOGY
        biopsyCheckbox = form.biopsyCheckbox.data
        papsCheckbox = form.papsCheckbox.data
        FNABCheckbox = form.FNABCheckbox.data
        cellCheckbox = form.cellCheckbox.data
        cytolCheckbox = form.cytolCheckbox.data

    # CLINICAL MICROSCOPY AND PARASITOLOGY
        urinCheckbox = form.urinCheckbox.data
        stoolCheckbox = form.stoolCheckbox.data
        occultCheckbox = form.occultCheckbox.data
        semenCheckbox = form.semenCheckbox.data
        ELISACheckbox = form.ELISACheckbox.data

    # SEROLOGY
        ASOCheckbox = form.ASOCheckbox.data
        AntiHBSCheckbox = form.AntiHBSCheckbox.data
        HCVCheckbox = form.HCVCheckbox.data
        C3Checkbox = form.C3Checkbox.data
        HIVICheckbox = form.HIVICheckbox.data
        HIVIICheckbox = form.HIVIICheckbox.data
        NS1Checkbox = form.NS1Checkbox.data
        VDRLCheckbox = form.VDRLCheckbox.data
        PregCheckbox = form.PregCheckbox.data
        RFCheckbox = form.RFCheckbox.data
        QuantiCheckbox = form.QuantiCheckbox.data
        QualiCheckbox = form.QualiCheckbox.data
        TyphidotCheckbox = form.TyphidotCheckbox.data
        TubexCheckbox = form.TubexCheckbox.data
        HAVIgMCheckbox = form.HAVIgMCheckbox.data
        DengueCheckbox = form.DengueCheckbox.data

    # IMMUNOCHEMISTRY
        AFPCheckbox = form.AFPCheckbox.data
        ferritinCheckbox = form.ferritinCheckbox.data
        HBcIgMCheckbox = form.HBcIgMCheckbox.data
        AntiHBECheckbox = form.AntiHBECheckbox.data
        CA125Checkbox = form.CA125Checkbox.data
        PROBNPCheckbox = form.PROBNPCheckbox.data
        CA153Checkbox = form.CA153Checkbox.data
        CA199Checkbox = form.CA199Checkbox.data
        PSACheckbox = form.PSACheckbox.data
        CEACheckbox = form.CEACheckbox.data
        FreeT3Checkbox = form.FreeT3Checkbox.data
        ANA2Checkbox = form.ANA2Checkbox.data
        FreeT4Checkbox = form.FreeT4Checkbox.data
        HBsAGCheckbox = form.HBsAGCheckbox.data
        TroponiniCheckbox = form.TroponiniCheckbox.data
        HbACheckbox = form.HbACheckbox.data
        HBAeAgCheckbox = form.HBAeAgCheckbox.data
        BetaCheckbox = form.BetaCheckbox.data
        T3Checkbox = form.T3Checkbox.data
        T4Checkbox = form.T4Checkbox.data
        TSHCheckbox = form.TSHCheckbox.data

    # CLINICAL CHEMISTRY
        ALPCheckbox = form.ALPCheckbox.data
        AmylaseCheckbox = form.AmylaseCheckbox.data
        BUACheckbox = form.BUACheckbox.data
        BUNCheckbox = form.BUNCheckbox.data
        CreatinineCheckbox = form.CreatinineCheckbox.data
        SGPTCheckbox = form.SGPTCheckbox.data
        SGOTCheckbox = form.SGOTCheckbox.data
        FBSCheckbox = form.FBSCheckbox.data
        RBSCheckbox = form.RBSCheckbox.data
        HPPCheckbox = form.HPPCheckbox.data
        OGCTCheckbox = form.OGCTCheckbox.data
        HGTCheckbox = form.HGTCheckbox.data
        OGTTCheckbox = form.OGTTCheckbox.data
        NaCheckbox = form.NaCheckbox.data
        MgCheckbox = form.MgCheckbox.data
        LipidCheckbox = form.LipidCheckbox.data
        TriglyCheckbox = form.TriglyCheckbox.data
        CholCheckbox = form.CholCheckbox.data
        ClCheckbox = form.ClCheckbox.data
        TPAGCheckbox = form.TPAGCheckbox.data
        TotalCheckbox = form.TotalCheckbox.data
        GlobCheckbox = form.GlobCheckbox.data
        AlbCheckbox = form.AlbCheckbox.data
        CKMBCheckbox = form.CKMBCheckbox.data
        CKTotalCheckbox = form.CKTotalCheckbox.data
        LDHCheckbox = form.LDHCheckbox.data
        KCheckbox = form.KCheckbox.data
        CaCheckbox = form.CaCheckbox.data
        IonizedCheckbox = form.IonizedCheckbox.data
        PhosCheckbox = form.PhosCheckbox.data

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

    return render_template("doctor/patient/labtest_request.html", patient_id=patient_id, Patientform=form, doctor=doctor_info)

# PRESCRIPTION
@doctor_bp.route('/prescription/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def prescription():
    form = PatientForm()
    patient_id = None
    user_id = current_user.id
    doctor_info = doctor.get_doctor_info(user_id)

    if request.method == 'GET':
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

    return render_template("doctor/patient/prescription.html", consultation=consultation_info, patient=patient_info, prescriptions=prescription_info, patient_id=patient_id, PatientForm=form, info=doctor_info)

# DELETE PATIENT RECORD
@doctor_bp.route('/delete_patient/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def delete_patient():
    form = PatientForm()
    user_id = current_user.id
    doctor_info = doctor.get_doctor_info(user_id)

    if request.method == "POST":
        patient_id = request.form.get("patient_id")
        doctor_info = doctor.get_doctor_info(user_id)

        result = doctor.delete_patient_record(patient_id)

        if result:
            return render_template("doctor/patient/patient.html", success=True, PatientForm=form, info=doctor_info)
        else:
            return render_template("doctor/patient/patient.html", error=True, PatientForm=form, info=doctor_info)
        
    return render_template("doctor/patient/patient.html", PatientForm=form, info=doctor_info)