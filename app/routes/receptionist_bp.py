from flask import render_template, redirect, request, url_for, jsonify, session
import math
from app.forms.receptionist_f import *
import app.models as models
from app.models.receptionist_m import *
from flask import Blueprint
import secrets
import string
from flask_login import login_required, logout_user, current_user, current_user
from app.routes.utils import role_required

receptionist_bp = Blueprint('receptionist', __name__)

headings = ("Reference Number", "Date", "Time", "Last Name", "Status", "Doctor", "Actions")
headings_schedule = ("Schedule ID", "Date", "Time", "Slots", "Doctor", "Actions")

# Main routes
@receptionist_bp.route('/')
@login_required
@role_required('receptionist')
def dashboard():
    current_id = current_user.id 
    receptionist_info = receptionist.get_user(current_id)
    patients_data = receptionist.get_patients()
    limited_patient = patients_data[:5]

    return render_template("receptionist/dashboard/dashboard.html", info=receptionist_info, patients=limited_patient)

@receptionist_bp.route('/calendar/')
@login_required
@role_required('receptionist')
def calendar():
    current_id = current_user.id 
    receptionist_info = receptionist.get_user(current_id)
    return render_template("receptionist/calendar/calendar.html", info=receptionist_info)

@receptionist_bp.route('/appointment/')
@login_required
@role_required('receptionist')
def appointment():
    current_id = current_user.id 
    receptionist_info = receptionist.get_user(current_id)
    user_id = current_user.id
    form = EditAppointmentForm()
    # Get the page number from the query string, default to 1 if not specified
    page = int(request.args.get('page', 1))

    # Set the number of items to display per page
    items_per_page = 9 

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

    return render_template("receptionist/appointment/appointment.html", headings=headings, data=data_dict, page=page, total_pages=total_pages, form=form, info=receptionist_info)

@receptionist_bp.route('/schedule/')
@login_required
@role_required('receptionist')
def schedule():
    current_id = current_user.id 
    receptionist_info = receptionist.get_user(current_id)
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
    return render_template("receptionist/schedule/schedule.html", headings=headings_schedule, data=data_dict, page=page, total_pages=total_pages, form=form, info=receptionist_info)

@receptionist_bp.route('/patient/')
@login_required
@role_required('receptionist')
def patient():
    current_id = current_user.id 
    receptionist_info = receptionist.get_user(current_id)
    patients_data = receptionist.get_patients()

    return render_template("receptionist/patient/patient.html", patients=patients_data, info=receptionist_info)

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
        new_patient.userID = current_id

        result = new_patient.add()

        if result:
            return render_template("receptionist/patient/add_patient.html", success=True, PatientForm=form, info=receptionist_info)
        else:
            return render_template("receptionist/patient/add_patient.html", error=True, PatientForm=form, info=receptionist_info)

    return render_template("receptionist/patient/add_patient.html", info=receptionist_info, PatientForm=form)

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

        return render_template('receptionist/patient/patient_record.html', patient=patient_info, patient_id=patient_id, PatientForm=form, info=receptionist_info)

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
            return render_template("receptionist/patient/patient_record.html", new_patient_id=new_patient_id, success=True, patient=updated_info, PatientForm=form, info=receptionist_info)
        else:
            return render_template("receptionist/patient/patient_record.html", new_patient_id=new_patient_id, error=True, patient=updated_info, PatientForm=form, info=receptionist_info)

    return render_template("receptionist/patient/patient_record.html", PatientForm=form, info=receptionist_info)

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
            return render_template("receptionist/patient/patient.html", success=True, PatientForm=form, info=receptionist_info)
        else:
            return render_template("receptionist/patient/patient.html", error=True, PatientForm=form, info=receptionist_info)
        
    return render_template("receptionist/patient/patient.html", PatientForm=form, info=receptionist_info)

@receptionist_bp.route('/profile/')
@login_required
@role_required('receptionist')
def profile():
    current_id = current_user.id 
    receptionist_info = receptionist.get_user(current_id)
    return render_template("receptionist/profile/profile.html", info=receptionist_info)

@receptionist_bp.route('/logout/')
@login_required
def logout():
    print("Logout route accessed")  
    logout_user()
    return redirect(url_for('login'))

# Function and function routes

def generate_reference_number():
    characters = string.ascii_uppercase + string.digits
    reference_number = ''.join(secrets.choice(characters) for _ in range(6))
    return reference_number

def generate_status():
    return 'PENDING'

def generate_cancel_status():
    return 'CANCELLED'

@receptionist_bp.route('/add-appointment/', methods=['GET', 'POST'])
@login_required
@role_required('receptionist')
def add_appointment():
    form = AppointmentForm(request.form)
    user_id = current_user.id
    print("User ID:", user_id)
    booking_details = None
    time_schedules = None
    doctor_id = None
    doctor_names = Appointment.get_all_doctor_names()

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
                    print('Reference already exists')
                else:
                    new_appointment = Appointment(
                        reference_number=form.reference_number.data,
                        receptionistID=user_id,
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
                    print('New appointment added!', 'success')
                    
                    # Fetch booking details after adding the appointment
                    booking_details = Appointment.get_booking_reference_details(form.reference_number.data)
                    
                    print(booking_details)
                    
                    return jsonify(success=True, message="Appointment added successfully", booking_details=booking_details)
            else:
                print(form.errors)  # Add this line to print form errors for debugging
                print('Failed to add appointment. Please check the form for errors.', 'danger')
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print('An error occurred while processing the appointment.', 'danger')
            # Set time_schedules to an empty list in case of an error
            time_schedules = []
            return jsonify(success=False, message="Internal Server Error"), 500

    return render_template("receptionist/appointment/appointment_add_v2.html", form=form, booking_details=booking_details, time_schedules=time_schedules, doctor_names=doctor_names, doctor_id=doctor_id)



@receptionist_bp.route('/delete-appointment/', methods=['POST'])
@login_required
@role_required('receptionist')
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
        receptionist_bp.logger.error("An error occurred: %s" % str(e))
        return jsonify(success=False, message="Internal Server Error"), 500

@receptionist_bp.route('/view-appointment/', methods=["GET"])
@login_required
@role_required('receptionist')
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
        print("Appointment not found.", "error")
        return jsonify(success=False, message="Appointment not found.")
    
    return render_template("receptionist/appointment/appointment_view.html", row=appointment_data_dict)


@receptionist_bp.route('/get-booking-details/<reference_number>', methods=['GET'])
@login_required
@role_required('receptionist')
def get_booking_details(reference_number):
    booking_details = Appointment.get_booking_reference_details(reference_number)

    if booking_details:
        return jsonify(booking_details)
    else:
        return jsonify({'error': 'Booking details not available'}), 404


@receptionist_bp.route('/edit-appointment-version-two/', methods=["GET", "POST"])
@login_required
@role_required('receptionist')
def reschedule_version_two():
    reference_number = request.form.get('reference_number')
    doctor_name = request.form.get('doctor_name')
    print('Doctor name in reschedule_version_two: ', doctor_name)
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
    return render_template("receptionist/appointment/appointment.html", form=form, data=appointment_data_dict, time_data=time_data)


@receptionist_bp.route('/search-appointments/', methods=['POST'])
@login_required
@role_required('receptionist')
def search_appointments():
    try:
        data = request.get_json()
        print("Received data:", data) 
        search_query = data.get('searchTerm')
        print("Search term:", search_query)
        filter_by = data.get('filterBy')
        print("Filter by:", filter_by)
        
        if filter_by == 'all':
            search_results = Appointment.search_appointment(search_query)
            print("Search results:", search_results)
        else:
            search_results = Appointment.filter_appointment(filter_by, search_query)
            print("Search results:", search_results)
            
        return jsonify({'success': True, 'data': search_results})
    except Exception as e:
        print("Error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

    
@receptionist_bp.route('/get-time-schedules', methods=['POST'])
@login_required
@role_required('receptionist')
def get_time_schedules():
    try:
        selected_date = request.form['selected_date']
        selected_doctor = request.form['selected_doctor']  # Add this line to get the selected doctor
        print("Selected doctor in time:", selected_doctor)
        time_schedules = Appointment.all_time_schedules(selected_date, selected_doctor)
        return jsonify(success=True, time_schedules=time_schedules)
    except Exception as e:
        return jsonify(success=False, message=str(e))

@receptionist_bp.route('/cancel-appointment/', methods=['GET', 'POST'])
@login_required
@role_required('receptionist')
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
        receptionist_bp.logger.error("An error occurred: %s" % str(e))
        return jsonify(success=False, message="Internal Server Error"), 500

@receptionist_bp.route('/get-appointment-data/', methods=['GET'])
@login_required
@role_required('receptionist')
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
    
    
@receptionist_bp.route('/get-doctor-id/', methods=['POST'])
@login_required
@role_required('receptionist')
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
@receptionist_bp.route('/add-schedule/', methods=['GET', 'POST'])
@login_required
@role_required('receptionist')
def add_schedule():
    form = ScheduleForm(request.form)
    user_id = current_user.id
    print("User ID:", user_id)
    form.receptionistID.data = user_id
    doctor_id = None
    doctor_names = Appointment.get_all_doctor_names()

    if request.method == 'POST':
        try:
            # Extract the chosen doctor from the form data
            chosen_doctor = request.form['doctorName']
            print('Before print statements. Chosen doctor:', chosen_doctor)
            doctor_id_dict = Appointment.get_doctor_id(chosen_doctor)

            # Extract the ID from the dictionary
            doctor_id = doctor_id_dict['id']
            print('In the add route, doctor ID is:', doctor_id)
            
            print('Data added: ', form.date_appointment.data, form.time_appointment.data, form.slots.data, form.doctorID.data, form.doctorName.data, form.receptionistID.data)
            if form.validate_on_submit():
                
                new_appointment = Schedule(
                        date_appointment=form.date_appointment.data,
                        time_appointment=form.time_appointment.data,
                        slots=form.slots.data,
                        doctorID=form.doctorID.data,
                        doctorName=form.doctorName.data,  # Use the 'data' attribute to access form data
                        receptionistID=form.receptionistID.data
                    )
                added_successfully = new_appointment.add_schedule()

                if added_successfully:
                    return jsonify(success=True, message="Appointment added successfully")
                else:
                    return jsonify(success=False, message="Appointment already exists"), 400
            else:
                print(form.errors)  # Add this line to print form errors for debugging
                return jsonify(success=False, message="Form validation failed"), 400
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print('An error occurred while processing the appointment.')
            return jsonify(success=False, message="Internal Server Error"), 500

    return render_template("receptionist/schedule/schedule_add.html", form=form, doctor_names=doctor_names, doctor_id=doctor_id)

@receptionist_bp.route('/search-schedules/', methods=['POST'])
@login_required
@role_required('receptionist')
def search_schedules():
    try:
        user_id = current_user.id
        data = request.get_json()
        print("Received data:", data) 
        search_query = data.get('searchTerm')
        print("Search term:", search_query)
        filter_by = data.get('filterBy')
        print("Filter by:", filter_by)
        
        if filter_by == 'all':
            search_results = Schedule.search_schedule(search_query, user_id)
            print("Search results:", search_results)
        else:
            search_results = Schedule.filter_schedule(filter_by, search_query, user_id)
            print("Search results:", search_results)
            
        return jsonify({'success': True, 'data': search_results})
    except Exception as e:
        print("Error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

@receptionist_bp.route('/view-schedules/', methods=["GET"])
@login_required
@role_required('receptionist')
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
    
    return render_template("receptionist/schedule/schedule_view.html", row=schedule_data_dict)


@receptionist_bp.route('/delete-schedule/', methods=['POST'])
@login_required
@role_required('receptionist')
def delete_schedule():
    try:
        schedule_id = request.form.get('reference_number')
        doctor_name = request.form.get('doctor_name')
        print('Doctor Name: ', doctor_name)

        if Appointment.delete(schedule_id):
            return jsonify(success=True, message="Successfully deleted")
        else:
            return jsonify(success=False, message="Failed to delete appointment")
    except Exception as e:
        # Log the error for debugging purposes
        receptionist_bp.logger.error("An error occurred: %s" % str(e))
        return jsonify(success=False, message="Internal Server Error"), 500
    

@receptionist_bp.route('/get-schedule-data/', methods=['GET'])
@login_required
@role_required('receptionist')
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

@receptionist_bp.route('/update-schedule/', methods=["GET", "POST"])
@login_required
@role_required('receptionist')
def update_schedule():
    current_id = current_user.id 
    receptionist_info = receptionist.get_user(current_id)
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
            scheduleID, new_date_appointment, new_time_appointment, new__slots):
            return jsonify(success=True, message="Appointment updated successfully")
        else:
            return jsonify(success=False, message="Failed to update appointment.")
    else:
        print ("Failed to update appointment")
        print("Form validation failed:", form.errors)
    return render_template("receptionist/schedule/schedule.html", form=form, data=appointment_data_dict, info=receptionist_info)
    
