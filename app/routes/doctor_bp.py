from flask import render_template, request, jsonify, redirect, url_for, flash
from app.forms.doctor_f import *
import app.models as models
from app.models.doctor_m import *
from app.models.login_m import *
import math
import secrets
import string
from flask import Blueprint
from app.forms.doctor_f import AppointmentForm, EditAppointmentForm
from flask_login import login_required, logout_user, current_user
from app.routes.utils import role_required
from cloudinary import uploader
from cloudinary.uploader import upload
from cloudinary.uploader import destroy

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/')
@login_required
@role_required('doctor')
def dashboard():
    current_id = current_user.id 
    doctor_info = doctor.get_doctor_info(current_id)
    patients_data = doctor.get_patients(current_id)
    limited_patient = patients_data[:5]
    sched_today = Appointment.show_schedule_for_today(current_id)
    print(f'Schedule for today: {sched_today}')

    sched_today_data_list = []  # Initialize the list here

    if sched_today:
        for appointment in sched_today:
            sched_today_data_dict = {
                "date_appointment": appointment['date_appointment'],
                "time_appointment": appointment['time_appointment'],
                "first_name": appointment['first_name'],
                "middle_name": appointment['middle_name'],
                "last_name": appointment['last_name'],
                "status_": appointment['status_'],
                "contact_number": appointment['contact_number']
            }
            sched_today_data_list.append(sched_today_data_dict)
            print(f'List of appointment: {sched_today_data_list}')
    else:
        print('No sched for today')

    return render_template("doctor/dashboard/dashboard.html", info=doctor_info, patients=limited_patient, sched_data=sched_today_data_list)


@doctor_bp.route('/calendar/')
@login_required
@role_required('doctor')
def calendar():
    current_id = current_user.id 
    doctor_info = doctor.get_doctor_info(current_id)
    return render_template("doctor/calendar/calendar.html", info=doctor_info)

headings = ("Reference Number", "Date", "Time", "Last Name", "Status", "Doctor", "Actions")
headings_schedule = ("Schedule ID", "Date", "Time", "Slots", "Doctor", "Actions")

@doctor_bp.route('/appointment/')
@login_required
@role_required('doctor')
def appointment():
    current_id = current_user.id 
    doctor_info = doctor.get_doctor_info(current_id)
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

    return render_template("doctor/appointment/appointment.html", headings=headings, data=data_dict, page=page, total_pages=total_pages, form=form, info=doctor_info)

@doctor_bp.route('/schedule/')
@login_required
@role_required('doctor')
def schedule():
    current_id = current_user.id 
    doctor_info = doctor.get_doctor_info(current_id)
    form = ScheduleForm()
    
    page = int(request.args.get('page', 1))

    items_per_page = 1000  

    all_schedules = Schedule.all_doctor_schedules(current_id)

    total_pages = math.ceil(len(all_schedules) / items_per_page)

    # Calculate the starting and ending index for the current page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    # Get the data for the current page
    data = all_schedules[start_index:end_index]

    data_dict = [
        {
            'scheduleID': schedule[0],
            'date_appointment': schedule[1],
            'time_appointment': str(schedule[2]),  
            'slots': schedule[3],
            'doctorName': schedule[4],
        }
        for schedule in data
    ]
    return render_template("doctor/schedule/schedule.html", headings=headings_schedule, data=data_dict, page=page, total_pages=total_pages, form=form, info=doctor_info)


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
    User.record_logout(current_user.role.upper(), current_user.username)
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

        result = new_patient.add(user_id, current_user.username)

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
        doctor_info = doctor.get_doctor_info(user_id)
        new_patient_id = request.form.get('patient_id')
        new_history_id = request.form.get('history_id')

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
        new_specifications = form.specifications.data.capitalize()
        new_others = form.others.data.capitalize()

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
        diet = form.diet.data.capitalize()

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
        meds = form.medications.data.capitalize()

    # ALLERGIES
        allergy = form.allergies.data.capitalize()

        existing_history = doctor.get_patient_history(new_patient_id)
        
        if existing_history:
            updated = doctor.update_medical_history(current_user.username, historyID = new_history_id, patientID = new_patient_id, bcgCheckbox = bcg_checkbox_value,
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
            result = doctor.add_medical_history(current_user.username, patientID = new_patient_id, bcgCheckbox = bcg_checkbox_value,
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

# ADD MEDICAL CLEARANCE 
@doctor_bp.route('/add_clearance/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def add_clearance():
    form = PatientForm()
    current_id = current_user.id 
    doctor_info = doctor.get_doctor_info(current_id)

    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        patient_info = doctor.get_patient_info(patient_id)
        patient_history = doctor.get_patient_history (patient_id)
        doctor_info = doctor.get_doctor_info(current_id)

        return render_template('doctor/patient/add_clearance.html', profile=patient_info, PatientForm=form, patient_id=patient_id, info=doctor_info, patient=patient_history)
    
    elif request.method == 'POST':
        doctor_info = doctor.get_doctor_info(current_id)
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

        new_history_id = request.form.get('history_id')

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
        new_specifications = form.specifications.data.capitalize()
        new_others = form.others.data.capitalize()

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
        diet = form.diet.data.capitalize()

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
        meds = form.medications.data.capitalize()

    # ALLERGIES
        allergy = form.allergies.data.capitalize()

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
        examinations = request.form.get('examinations').capitalize()

    # CLEARANCE
        subject = request.form.get('subject').upper()
        reason = request.form.get('reasons').capitalize()
        recommendations = request.form.get('recommendations').capitalize()
        clearance = request.form.get('clearance_textarea').capitalize()

        info_update = doctor.update_patient_info(current_user.username, patientID=new_patient_id, firstName=new_first_name, midName=new_middle_name, lastName=new_last_name, age=new_age, 
                                             civilStatus=new_civil_status, gender=new_gender, bloodType=new_bloodType, religion=new_religion, birthPlace=new_birth_place, 
                                             occupation=new_occupation, p_email=new_email, p_contactNum=new_contact_num, birthDate=new_birth_date, p_address=new_p_address, 
                                             nationality=new_nationality, eContactName=new_e_person, relationship=new_relationship, eContactNum=new_e_number)
        
        updated_info = doctor.get_patient_info(new_patient_id)

        existing_history = doctor.get_patient_history(new_patient_id)

        if existing_history:
            history_update = doctor.update_medical_history(current_user.username, historyID = new_history_id, patientID = new_patient_id, bcgCheckbox = bcg_checkbox_value,
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

            updated_history = doctor.get_patient_history(new_patient_id)
        
        
        clearance_result = doctor.add_medical_clearance(current_user.username, patientID=new_patient_id, subjectClearance=subject, reason=reason, recommendations=recommendations, bloodPressure=blood_p,
                                               pulseRate=pulse_r, temperature=temp, respRate=respiratory_r, height=height, weight_p=weight, bmi=body_mass, oxygenSaturation=oxygenSaturation, 
                                               painSection=painSection, physicalExam=examinations, clearance=clearance)

        if info_update and history_update and clearance_result:
            return render_template("doctor/patient/add_clearance.html", patient_id=new_patient_id, success=True, profile=updated_info, patient=updated_history, PatientForm=form, info=doctor_info)
        else:
            return render_template("doctor/patient/add_clearance.html", patient_id=new_patient_id, error=True, profile=updated_info, patient=updated_history, PatientForm=form, info=doctor_info)

    return render_template("doctor/patient/add_clearance.html", profile=patient_info, patient=patient_history, PatientForm=form, patient_id=patient_id, info=doctor_info)

# ADD MEDICAL CERTIFICATE 
@doctor_bp.route('/add_certificate/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def add_certificate():
    form = PatientForm()
    current_id = current_user.id 
    doctor_info = doctor.get_doctor_info(current_id)

    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        patient_info = doctor.get_patient_info(patient_id)
        patient_history = doctor.get_patient_history (patient_id)
        doctor_info = doctor.get_doctor_info(current_id)

        return render_template('doctor/patient/add_certificate.html', profile=patient_info, PatientForm=form, patient_id=patient_id, info=doctor_info, patient=patient_history)
    
    elif request.method == 'POST':
        doctor_info = doctor.get_doctor_info(current_id)
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

        new_history_id = request.form.get('history_id')

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
        new_specifications = form.specifications.data.capitalize()
        new_others = form.others.data.capitalize()

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
        diet = form.diet.data.capitalize()

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
        meds = form.medications.data.capitalize()

    # ALLERGIES
        allergy = form.allergies.data.capitalize()

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
        examinations = request.form.get('examinations').capitalize()

    # CERTIFICATE
        subject = request.form.get('subject').upper()
        reason = request.form.get('reasons').capitalize()
        recommendations = request.form.get('recommendations').capitalize()
        certificate = request.form.get('certificate_textarea').capitalize()

        info_update = doctor.update_patient_info(current_user.username, patientID=new_patient_id, firstName=new_first_name, midName=new_middle_name, lastName=new_last_name, age=new_age, 
                                             civilStatus=new_civil_status, gender=new_gender, bloodType=new_bloodType, religion=new_religion, birthPlace=new_birth_place, 
                                             occupation=new_occupation, p_email=new_email, p_contactNum=new_contact_num, birthDate=new_birth_date, p_address=new_p_address, 
                                             nationality=new_nationality, eContactName=new_e_person, relationship=new_relationship, eContactNum=new_e_number)
        
        updated_info = doctor.get_patient_info(new_patient_id)

        existing_history = doctor.get_patient_history(new_patient_id)

        if existing_history:
            history_update = doctor.update_medical_history(current_user.username, historyID = new_history_id, patientID = new_patient_id, bcgCheckbox = bcg_checkbox_value,
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

            updated_history = doctor.get_patient_history(new_patient_id)
        
        
        clearance_result = doctor.add_medical_certificate(current_user.username, patientID=new_patient_id, subjectCertificate=subject, reason=reason, recommendations=recommendations, bloodPressure=blood_p,
                                               pulseRate=pulse_r, temperature=temp, respRate=respiratory_r, height=height, weight_p=weight, bmi=body_mass, oxygenSaturation=oxygenSaturation, 
                                               painSection=painSection, physicalExam=examinations, certificate=certificate)

        if info_update and history_update and clearance_result:
            return render_template("doctor/patient/add_certificate.html", patient_id=new_patient_id, success=True, profile=updated_info, patient=updated_history, PatientForm=form, info=doctor_info)
        else:
            return render_template("doctor/patient/add_certificate.html", patient_id=new_patient_id, error=True, profile=updated_info, patient=updated_history, PatientForm=form, info=doctor_info)

    return render_template("doctor/patient/add_certificate.html", profile=patient_info, patient=patient_history, PatientForm=form, patient_id=patient_id, info=doctor_info)


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
        complain = form.complaints.data.capitalize()

    # HISTORY OF PRESENT ILLNESS
        p_illness = form.h_illness.data.capitalize()

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
        abnormalities_head = form.abnormalities_head.data.capitalize()
        normal_ears = form.normal_ears.data.upper()
        abnormalities_ears = form.abnormalities_ears.data.capitalize()
        normal_eyes = form.normal_eyes.data.upper()
        abnormalities_eyes = form.abnormalities_eyes.data.capitalize()
        normal_nose = form.normal_nose.data.upper()
        abnormalities_nose = form.abnormalities_nose.data.capitalize()
        normal_skin = form.normal_skin.data.upper()
        abnormalities_skin = form.abnormalities_skin.data.capitalize()
        normal_back = form.normal_back.data.upper()
        abnormalities_back = form.abnormalities_back.data.capitalize()
        normal_neck = form.normal_neck.data.upper()
        abnormalities_neck = form.abnormalities_neck.data.capitalize()
        normal_throat = form.normal_throat.data.upper()
        abnormalities_throat = form.abnormalities_throat.data.capitalize()
        normal_chest = form.normal_chest.data.upper()
        abnormalities_chest = form.abnormalities_chest.data.capitalize()
        normal_abdomen = form.normal_abdomen.data.upper()
        abnormalities_abdomen = form.abnormalities_abdomen.data.capitalize()
        normal_upper = form.normal_upper.data.upper()
        abnormalities_upper = form.abnormalities_upper.data.capitalize()
        normal_lower = form.normal_lower.data.upper()
        abnormalities_lower = form.abnormalities_lower.data.capitalize()
        normal_tract = form.normal_tract.data.upper()
        abnormalities_tract = form.abnormalities_tract.data.capitalize()
        comments = form.comments.data.capitalize()

    # DIAGNOSIS
        diagnosis = form.diagnosis.data.capitalize()

        result = doctor.add_medical_assessment(current_user.username, patientID=new_patient_id, subjectComp=sub, complaints=complain, illnessHistory=p_illness, bloodPressure=blood_p,
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
    form = PatientForm()
    user_id = current_user.id
    doctor_info = doctor.get_doctor_info(user_id)
    patients_data = doctor.get_patients(user_id)

    return render_template("doctor/patient/patient.html", patients=patients_data, info=doctor_info, PatientForm=form)

# CONSULTATION TABLE
@doctor_bp.route('/consultation/')
@login_required
@role_required('doctor')
def consultation():
    patient_id = request.args.get('patient_id')
    patient_info = doctor.get_patient_info(patient_id)
    consultation_data = doctor.get_consultations(patient_id)
    clearance_data = doctor.get_clearances(patient_id)
    certificate_data = doctor.get_certificates(patient_id)
    user_id = current_user.id
    doctor_info = doctor.get_doctor_info(user_id)

    return render_template("doctor/patient/consultation.html", certificates=certificate_data, consultations=consultation_data, clearances=clearance_data, patient=patient_info, patient_id=patient_id, info=doctor_info)

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

        updated = doctor.update_patient_info(current_user.username, patientID=new_patient_id, firstName=new_first_name, midName=new_middle_name, lastName=new_last_name, age=new_age, 
                                             civilStatus=new_civil_status, gender=new_gender, bloodType=new_bloodType, religion=new_religion, birthPlace=new_birth_place, 
                                             occupation=new_occupation, p_email=new_email, p_contactNum=new_contact_num, birthDate=new_birth_date, p_address=new_p_address, 
                                             nationality=new_nationality, eContactName=new_e_person, relationship=new_relationship, eContactNum=new_e_number,)  
        
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
        complain = form.complaints.data.capitalize()

    # HISTORY OF PRESENT ILLNESS
        p_illness = form.h_illness.data.capitalize()

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
        abnormalities_head = form.abnormalities_head.data.capitalize()
        normal_ears = form.normal_ears.data.upper()
        abnormalities_ears = form.abnormalities_ears.data.capitalize()
        normal_eyes = form.normal_eyes.data.upper()
        abnormalities_eyes = form.abnormalities_eyes.data.capitalize()
        normal_nose = form.normal_nose.data.upper()
        abnormalities_nose = form.abnormalities_nose.data.capitalize()
        normal_skin = form.normal_skin.data.upper()
        abnormalities_skin = form.abnormalities_skin.data.capitalize()
        normal_back = form.normal_back.data.upper()
        abnormalities_back = form.abnormalities_back.data.capitalize()
        normal_neck = form.normal_neck.data.upper()
        abnormalities_neck = form.abnormalities_neck.data.capitalize()
        normal_throat = form.normal_throat.data.upper()
        abnormalities_throat = form.abnormalities_throat.data.capitalize()
        normal_chest = form.normal_chest.data.upper()
        abnormalities_chest = form.abnormalities_chest.data.capitalize()
        normal_abdomen = form.normal_abdomen.data.upper()
        abnormalities_abdomen = form.abnormalities_abdomen.data.capitalize()
        normal_upper = form.normal_upper.data.upper()
        abnormalities_upper = form.abnormalities_upper.data.capitalize()
        normal_lower = form.normal_lower.data.upper()
        abnormalities_lower = form.abnormalities_lower.data.capitalize()
        normal_tract = form.normal_tract.data.upper()
        abnormalities_tract = form.abnormalities_tract.data.capitalize()
        comments = form.comments.data.capitalize()

    # DIAGNOSIS
        diagnosis = form.diagnosis.data.capitalize()

        update = doctor.update_medical_assessment(current_user.username, assessmentID=new_assessment_id, patientID=new_patient_id, subjectComp=sub, complaints=complain, illnessHistory=p_illness, bloodPressure=blood_p,
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


# UPDATE MEDICAL CLEARANCE
@doctor_bp.route('/clearance/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def clearance():
    form = PatientForm()
    current_id = current_user.id 
    doctor_info = doctor.get_doctor_info(current_id)

    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        clearance_id = request.args.get('clearance_id')
        patient_info = doctor.get_patient_info(patient_id)
        patient_history = doctor.get_patient_history (patient_id)
        patient_clearance = doctor.get_clearance_info(clearance_id, patient_id)
        doctor_info = doctor.get_doctor_info(current_id)
        
        return render_template('doctor/patient/clearance.html', patient=patient_history, clearance=patient_clearance, profile=patient_info, PatientForm=form, patient_id=patient_id, info=doctor_info)
    
    elif request.method == 'POST':
        doctor_info = doctor.get_doctor_info(current_id)
        new_clearance_id = request.form.get('clearance_id')
        new_patient_id = request.form.get('patient_id')
        
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

        new_history_id = request.form.get('history_id')

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
        new_specifications = form.specifications.data.capitalize()
        new_others = form.others.data.capitalize()

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
        diet = form.diet.data.capitalize()

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
        meds = form.medications.data.capitalize()

    # ALLERGIES
        allergy = form.allergies.data.capitalize()

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
        examinations = request.form.get('examinations').capitalize()
    
    # CLEARANCE
        subject = request.form.get('subject').upper()
        reason = request.form.get('reasons').capitalize()
        recommendations = request.form.get('recommendations').capitalize()
        clearance = request.form.get('clearance_textarea').capitalize()

        info_update = doctor.update_patient_info(current_user.username, patientID=new_patient_id, firstName=new_first_name, midName=new_middle_name, lastName=new_last_name, age=new_age, 
                                             civilStatus=new_civil_status, gender=new_gender, bloodType=new_bloodType, religion=new_religion, birthPlace=new_birth_place, 
                                             occupation=new_occupation, p_email=new_email, p_contactNum=new_contact_num, birthDate=new_birth_date, p_address=new_p_address, 
                                             nationality=new_nationality, eContactName=new_e_person, relationship=new_relationship, eContactNum=new_e_number)
        
        updated_info = doctor.get_patient_info(new_patient_id)

        existing_history = doctor.get_patient_history(new_patient_id)

        if existing_history:
            history_update = doctor.update_medical_history(current_user.username, historyID = new_history_id, patientID = new_patient_id, bcgCheckbox = bcg_checkbox_value,
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

            updated_history = doctor.get_patient_history(new_patient_id)

            clearance_update = doctor.update_medical_clearance(current_user.username, clearanceID=new_clearance_id, patientID=new_patient_id, subjectClearance=subject, reason=reason, recommendations=recommendations, bloodPressure=blood_p,
                                               pulseRate=pulse_r, temperature=temp, respRate=respiratory_r, height=height, weight_p=weight, bmi=body_mass, oxygenSaturation=oxygenSaturation, 
                                               painSection=painSection, physicalExam=examinations, clearance=clearance)
            updated_clearance = doctor.get_clearance_info(new_clearance_id, new_patient_id)

            if info_update and history_update and clearance_update:
                    return render_template("doctor/patient/clearance.html", patient_id=new_patient_id, success=True, profile=updated_info, patient=updated_history, PatientForm=form, info=doctor_info, clearance=updated_clearance)
            else:
                return render_template("doctor/patient/clearance.html", patient_id=new_patient_id, error=True, profile=updated_info, patient=updated_history, PatientForm=form, info=doctor_info, clearance=updated_clearance)

        return render_template("doctor/patient/clearance.html", profile=patient_info, patient=patient_history, PatientForm=form, patient_id=patient_id, info=doctor_info)

# UPDATE MEDICAL CERTIFICATE
@doctor_bp.route('/certificate/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def certificate():
    form = PatientForm()
    current_id = current_user.id 
    doctor_info = doctor.get_doctor_info(current_id)

    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        certificate_id = request.args.get('certificate_id')
        patient_info = doctor.get_patient_info(patient_id)
        patient_history = doctor.get_patient_history (patient_id)
        patient_certificate = doctor.get_certificate_info(certificate_id, patient_id)
        doctor_info = doctor.get_doctor_info(current_id)
        
        return render_template('doctor/patient/certificate.html', patient=patient_history, certificate=patient_certificate, profile=patient_info, PatientForm=form, patient_id=patient_id, info=doctor_info)
    
    elif request.method == 'POST':
        doctor_info = doctor.get_doctor_info(current_id)
        new_certificate_id = request.form.get('certificate_id')
        new_patient_id = request.form.get('patient_id')
        
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

        new_history_id = request.form.get('history_id')

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
        new_specifications = form.specifications.data.capitalize()
        new_others = form.others.data.capitalize()

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
        diet = form.diet.data.capitalize()

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
        meds = form.medications.data.capitalize()

    # ALLERGIES
        allergy = form.allergies.data.capitalize()

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
        examinations = request.form.get('examinations').capitalize()
    
    # CERTIFICATE
        subject = request.form.get('subject').upper()
        reason = request.form.get('reasons').capitalize()
        recommendations = request.form.get('recommendations').capitalize()
        certificate = request.form.get('certificate_textarea').capitalize()

        info_update = doctor.update_patient_info(current_user.username, patientID=new_patient_id, firstName=new_first_name, midName=new_middle_name, lastName=new_last_name, age=new_age, 
                                             civilStatus=new_civil_status, gender=new_gender, bloodType=new_bloodType, religion=new_religion, birthPlace=new_birth_place, 
                                             occupation=new_occupation, p_email=new_email, p_contactNum=new_contact_num, birthDate=new_birth_date, p_address=new_p_address, 
                                             nationality=new_nationality, eContactName=new_e_person, relationship=new_relationship, eContactNum=new_e_number)
        
        updated_info = doctor.get_patient_info(new_patient_id)

        existing_history = doctor.get_patient_history(new_patient_id)

        if existing_history:
            history_update = doctor.update_medical_history(current_user.username, historyID = new_history_id, patientID = new_patient_id, bcgCheckbox = bcg_checkbox_value,
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

            updated_history = doctor.get_patient_history(new_patient_id)

            certificate_update = doctor.update_medical_certificate(current_user.username, certificateID=new_certificate_id, patientID=new_patient_id, subjectCertificate=subject, reason=reason, recommendations=recommendations, bloodPressure=blood_p,
                                               pulseRate=pulse_r, temperature=temp, respRate=respiratory_r, height=height, weight_p=weight, bmi=body_mass, oxygenSaturation=oxygenSaturation, 
                                               painSection=painSection, physicalExam=examinations, certificate=certificate)
            updated_certificate = doctor.get_certificate_info(new_certificate_id, new_patient_id)

            if info_update and history_update and certificate_update:
                    return render_template("doctor/patient/certificate.html", patient_id=new_patient_id, success=True, profile=updated_info, patient=updated_history, PatientForm=form, info=doctor_info, certificate=updated_certificate)
            else:
                return render_template("doctor/patient/certificate.html", patient_id=new_patient_id, error=True, profile=updated_info, patient=updated_history, PatientForm=form, info=doctor_info, certificate=updated_certificate)

        return render_template("doctor/patient/certificate.html", profile=patient_info, patient=patient_history, PatientForm=form, patient_id=patient_id, info=doctor_info)


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
                               immunochem=immunochem_info, clinicalchem=clinicalchem_info, report=labrep_info, info=doctor_info)

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

        result = doctor.add_laboratory_request(current_user.username, patientID=new_patient_id, patientName=patient_fullName, labSubject=lab_subject, gender=sex, age=age, physician=doctorName, orderDate=requestDate, 
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
        print('prescription:', prescription_info)
        doctor_info = doctor.get_doctor_info(user_id)

        return render_template('doctor/patient/prescription.html', doctor=doctor_info, patient=patient_info, consultation=consultation_info, prescriptions=prescription_info, patient_id=patient_id, PatientForm=form)
    
    elif request.method == 'POST':
        new_assessment_id = request.form.get('assessment_id')
        new_patient_id = request.form.get('patient_id')
        medication_name = request.form.get('medication_name').capitalize()
        dosage = request.form.get('dosage').upper()
        p_quantity = request.form.get('quantity')
        duration = request.form.get('duration').capitalize()
        instructions = request.form.get('instructions').capitalize()

        result = doctor.add_prescription(current_user.username, new_assessment_id, medication_name, dosage, p_quantity, duration, instructions, new_patient_id)
        
        doctor_info = doctor.get_doctor_info(user_id)
        patient_info = doctor.get_patient_info(new_patient_id)
        consultation_info = doctor.get_consultation_info(new_assessment_id, new_patient_id)
        prescription_info = doctor.get_prescription_info(new_assessment_id)
        print('new prescription INFORMATION:', prescription_info)
        print('RESULT:', result)

        if result:
            return render_template("doctor/patient/prescription.html", success=True, doctor=doctor_info, patient=patient_info, consultation=consultation_info, prescriptions=prescription_info, patient_id=patient_id, PatientForm=form)
        else:
            return render_template("doctor/patient/prescription.html", error=True, doctor=doctor_info, patient=patient_info, consultation=consultation_info, prescriptions=prescription_info, patient_id=patient_id, PatientForm=form)

    return render_template("doctor/patient/prescription.html", consultation=consultation_info, patient=patient_info, prescriptions=prescription_info, patient_id=patient_id, PatientForm=form, doctor=doctor_info)

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

        result = doctor.delete_patient_record(patient_id, current_user.username)

        if result:
            return render_template("doctor/patient/patient.html", success=True, PatientForm=form, info=doctor_info)
        else:
            return render_template("doctor/patient/patient.html", error=True, PatientForm=form, info=doctor_info)
        
    return render_template("doctor/patient/patient.html", PatientForm=form, info=doctor_info)

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
                    new_appointment.add(current_user.username)
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

        if Appointment.delete(current_user.username, reference_number):
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
            current_user.username, reference_number, new_date_appointment, new_time_appointment, new_status_,
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

# SCHEDULE ROUTES AND FUNCTIONS
@doctor_bp.route('/add-schedule/', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def add_schedule():
    form = ScheduleForm(request.form)
    user_id = current_user.id
    print("User ID:", user_id)
    doctor_id = None
    doctor_names = Appointment.get_all_doctor_name(user_id)
    receptionist_ids = Schedule.get_receptionist_ids()
    print("Receptionist IDs:", receptionist_ids)

    if request.method == 'POST':
        try:
            chosen_doctor = request.form['doctorName']
            print('Before print statements. Chosen doctor:', chosen_doctor)
            # Extract the chosen doctor from the form data
            doctor_id_dict = Appointment.get_doctor_id(chosen_doctor)
    
            # Check if 'id' is in the dictionary before accessing it
            if doctor_id_dict is not None and 'id' in doctor_id_dict:
                doctor_id = doctor_id_dict['id']
                print('In the add route, doctor ID is:', doctor_id)
            else:
                print("Error: No doctor found with the specified last name.")
                return jsonify(success=False, message="Doctor not found"), 400

            print('Data added: ', form.date_appointment.data, form.time_appointment.data, form.slots.data, form.doctorID.data, form.doctorName.data, form.receptionistID.data)
            
            if form.validate_on_submit():
                print(form.errors)
                new_appointment = Schedule(
                    date_appointment=form.date_appointment.data,
                    time_appointment=form.time_appointment.data,
                    slots=form.slots.data,
                    doctorID=form.doctorID.data,
                    doctorName=form.doctorName.data,
                    receptionistID=form.receptionistID.data
                )

                added_successfully = new_appointment.add_schedule(current_user.username)
                print('Added successfully: ', added_successfully)
                if added_successfully:
                    return jsonify(success=True, message="Schedule added successfully")
                else:
                    print('Form validation errors:', form.errors)
                    return jsonify(success=False, message="Schedule already exists"), 400
            else:
                print(form.errors)
                error_message = "Form validation failed. Please check the highlighted fields."
                return jsonify(success=False, message=error_message), 400
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print('An error occurred while processing the schedule.')
            return jsonify(success=False, message="Internal Server Error"), 500

    return render_template("doctor/schedule/schedule_add.html", form=form, doctor_names=doctor_names, doctor_id=doctor_id, receptionist_ids=receptionist_ids)


@doctor_bp.route('/view-schedules/', methods=["GET"])
@login_required
@role_required('doctor')
def view_schedule():
    schedule_id = request.args.get('scheduleID')
    view_schedule = Schedule.view_schedule_by_scheduleID(schedule_id)
    print(view_schedule)
    
    if view_schedule:
        schedule_data_dict = {
            "scheduleID": view_schedule['scheduleID'],
            "date_appointment": view_schedule['date_appointment'],
            "time_appointment": view_schedule['time_appointment'],
            "slots": view_schedule['slots'],
            "user_first_name": view_schedule['user_first_name'],
            "user_middle_name": view_schedule['user_middle_name'],
            "user_last_name": view_schedule['user_last_name']
        }
        print('Scheduled data: ', schedule_data_dict)
    else:
        print("Appointment not found.")
        return jsonify(success=False, message="Appointment not found.")
    
    return render_template("doctor/schedule/schedule_view.html", row=schedule_data_dict)


@doctor_bp.route('/delete-schedule/', methods=['POST'])
@login_required
@role_required('doctor')
def delete_schedule():
    try:
        schedule_id = request.form.get('scheduleID')
        print('schedule id: ', schedule_id)
        doctor_name = request.form.get('doctor_name')
        print('Doctor Name: ', doctor_name)

        if Schedule.delete_schedules(schedule_id):
            return jsonify(success=True, message="Successfully deleted")
        else:
            return jsonify(success=False, message="Failed to delete appointment")
    except Exception as e:
        # Log the error for debugging purposes
        doctor_bp.logger.error("An error occurred: %s" % str(e))
        return jsonify(success=False, message="Internal Server Error"), 500
    

@doctor_bp.route('/get-schedule-data/', methods=['GET'])
@login_required
@role_required('doctor')
def get_schedule_data():
    try:
        scheduleID = request.args.get('scheduleID')

        # Ensure the reference number is provided
        if not scheduleID:
            return jsonify(success=False, message="Reference number is required.")

        # Fetch appointment data using the provided reference number
        schedule_data = Schedule.get_schedule_by_schedule_id(scheduleID)

        if schedule_data:
            # Fetch time options based on the appointment's date
            scheduled_date = schedule_data.get('date_appointment')  # Adjust accordingly
            time_options = Appointment.get_all_available_schedules(scheduled_date)
            
            print('Time options: ', time_options)

            return jsonify(success=True, scheduleData=schedule_data, timeOptions=time_options)
        else:
            return jsonify(success=False, message="Appointment not found.")

    except Exception as e:
        print("Error:", str(e))
        return jsonify(success=False, message="An error occurred.")

@doctor_bp.route('/update-schedule/', methods=["GET", "POST"])
@login_required
@role_required('doctor')
def update_schedule():
    current_id = current_user.id 
    doctor_info = doctor.get_doctor_info(current_id)
    scheduleID = request.form.get('scheduleID')
    print(scheduleID)
    doctor_name = request.form.get('doctor_name')
    print('Doctor name in reschedule_version_two: ', doctor_name)
    form = EditScheduleForm()
    schedule_data = Schedule.get_schedule_by_schedule_id(scheduleID)

    if schedule_data:
        appointment_data_dict = {
            "scheduleID": schedule_data['scheduleID'],
            "date_appointment": schedule_data['date_appointment'],
            "time_appointment": schedule_data['time_appointment'],
            "slots": schedule_data['slots'],
            "doctorName": schedule_data['doctorName']
        }
    else:
        return jsonify(success=False, message="Appointment not found.")

    if request.method == "POST" and form.validate():
        new_date_appointment = form.date_appointment.data
        new_time_appointment = form.time_appointment.data
        new__slots = form.slots.data

        old_date_appointment = schedule_data['date_appointment']
        old_time_appointment = schedule_data['time_appointment']
        print('Old Appointment Details: ', old_date_appointment, old_time_appointment)
        print('New Appointment Details: ', new_date_appointment, new_time_appointment)
        if Schedule.update_schedule(
            current_user.username, scheduleID, new_date_appointment, new_time_appointment, new__slots):
            return jsonify(success=True, message="Appointment updated successfully")
        else:
            return jsonify(success=False, message="Failed to update appointment.")
    else:
        print ("Failed to update appointment")
        print("Form validation failed:", form.errors)
    return render_template("doctor/schedule/schedule.html", form=form, data=appointment_data_dict, info=doctor_info)