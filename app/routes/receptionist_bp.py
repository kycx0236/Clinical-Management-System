from flask import render_template, redirect, request, url_for, flash, jsonify, session
import math
from app.forms.receptionist_f import AppointmentForm, EditAppointmentForm
from app.models.receptionist_m import Appointment
import app.models.receptionist_m as models_receptionist
from flask import Blueprint
import secrets
import string
from flask_login import login_required, logout_user, current_user
from app.routes.utils import role_required

receptionist_bp = Blueprint('receptionist', __name__)

headings = ("Reference Number", "Date", "Time", "Last Name", "Status", "Doctor", "Actions")

# Main routes
@receptionist_bp.route('/')
@login_required
@role_required('receptionist')
def dashboard():
    return render_template("receptionist/dashboard/dashboard.html")

@receptionist_bp.route('/calendar/')
@login_required
@role_required('receptionist')
def calendar():
    return render_template("receptionist/calendar/calendar.html")

@receptionist_bp.route('/appointment/')
@login_required
@role_required('receptionist')
def appointment():
    user_id = current_user.id
    form = EditAppointmentForm()
    # Get the page number from the query string, default to 1 if not specified
    page = int(request.args.get('page', 1))

    # Set the number of items to display per page
    items_per_page = 9  # You can adjust this to your preferred value

    # Retrieve all appointment data from your model
    all_appointments = models_receptionist.Appointment.all(user_id)

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

    return render_template("receptionist/appointment/appointment.html", headings=headings, data=data_dict, page=page, total_pages=total_pages, form=form)


@receptionist_bp.route('/profile/')
@login_required
@role_required('receptionist')
def profile():
    return render_template("receptionist/profile/profile.html")

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
    doctor_names = models_receptionist.Appointment.get_all_doctor_names()

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
            doctor_id_dict = models_receptionist.Appointment.get_doctor_id(chosen_doctor)

            # Extract the ID from the dictionary
            doctor_id = doctor_id_dict['id']
            print('In the add route, doctor ID is:', doctor_id)
            print('After print statements.')
            
            # Extract the chosen date from the form data
            chosen_date = request.form['date_appointment']
            form.date_appointment.data = chosen_date  # Set the form field with the chosen date

            # Fetch available time schedules for the chosen date
            time_schedules = models_receptionist.Appointment.all_time_schedules(chosen_date, chosen_doctor)
            
            # Get the selected time from the form
            selected_time = request.form['time_appointment']

            # Update the slots in the schedule table
            models_receptionist.Appointment.update_slots(chosen_date, selected_time, chosen_doctor, increment=False)
            print(request.form)  # Print the form data for debugging

            if form.validate_on_submit():
                reference_exists = models_receptionist.Appointment.unique_code(check_reference)
                
                if reference_exists:
                    flash("Appointment already exists. Please enter a new appointment.")
                else:
                    new_appointment = models_receptionist.Appointment(
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
                    flash('New appointment added!', 'success')
                    
                    # Fetch booking details after adding the appointment
                    booking_details = models_receptionist.Appointment.get_booking_reference_details(form.reference_number.data)
                    
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
        deleted_appointment = models_receptionist.Appointment.get_appointment_by_reference(reference_number)
        deleted_time = deleted_appointment['time_appointment']

        if models_receptionist.Appointment.delete(reference_number):
            # Increment the slots for the deleted time
            models_receptionist.Appointment.update_slots(deleted_appointment['date_appointment'], deleted_time, doctor_name, increment=True)
            
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
    view_appointment = models_receptionist.Appointment.view_appointment_by_reference(booking_ref_number)
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
    
    return render_template("receptionist/appointment/appointment_view.html", row=appointment_data_dict)


@receptionist_bp.route('/get-booking-details/<reference_number>', methods=['GET'])
@login_required
@role_required('receptionist')
def get_booking_details(reference_number):
    booking_details = models_receptionist.Appointment.get_booking_reference_details(reference_number)

    if booking_details:
        return jsonify(booking_details)
    else:
        return jsonify({'error': 'Booking details not available'}), 404

@receptionist_bp.route('/edit-appointment/', methods=["GET", "POST"])
@login_required
@role_required('receptionist')
def reschedule():
    booking_ref_number = request.args.get('reference_number')
    form = AppointmentForm()
    appointment_data = models_receptionist.Appointment.get_appointment_by_reference(booking_ref_number)

    if appointment_data:
        appointment_data_dict = {
            "reference_number": appointment_data['reference_number'],
            "date_appointment": appointment_data['date_appointment'],
            "time_appointment": appointment_data['time_appointment'],
            "status_": appointment_data['status_'],
            "book_date": appointment_data['book_date'],
            "first_name": appointment_data['first_name'],
            "middle_name": appointment_data['middle_name'],
            "last_name": appointment_data['last_name'],
            "sex": appointment_data['sex'],
            "birth_date": appointment_data['birth_date'],
            "contact_number": appointment_data['contact_number'],
            "email": appointment_data['email'],
            "address": appointment_data['address']
        }
        time_data = models_receptionist.Appointment.get_all_available_schedules(appointment_data['date_appointment'])
        print(appointment_data_dict)
        print(time_data)
    else:
        return jsonify(success=False, message="Appointment not found.")

    if request.method == "POST" and form.validate():
        new_date_appointment = form.date_appointment.data
        new_time_appointment = form.time_appointment.data
        new_status_ = form.status_.data
        new_first_name = form.first_name.data
        new_middle_name = form.middle_name.data
        new_last_name = form.last_name.data
        new_sex = form.sex.data
        new_birth_date = form.birth_date.data
        new_contact_number = form.contact_number.data
        new_email = form.email.data
        new_address = form.address.data

        old_date_appointment = appointment_data['date_appointment']
        old_time_appointment = appointment_data['time_appointment']
        
        if models_receptionist.Appointment.update(
            booking_ref_number, new_date_appointment, new_time_appointment, new_status_,
            new_first_name, new_middle_name, new_last_name, new_sex, new_birth_date,
            new_contact_number, new_email, new_address
        ):
            # Update the slots for the old and new times
            models_receptionist.Appointment.update_time_slots(old_date_appointment, old_time_appointment, new_time_appointment)

            return jsonify(success=True, message="Appointment updated successfully")
        else:
            return jsonify(success=False, message="Failed to update appointment.")
    else:
        print ("Failed to update appointment")
        print("Form validation failed:", form.errors)
    return render_template("receptionist/appointment/appointment_edit.html", form=form, row=appointment_data_dict, time_data=time_data)

@receptionist_bp.route('/edit-appointment-version-two/', methods=["GET", "POST"])
@login_required
@role_required('receptionist')
def reschedule_version_two():
    reference_number = request.form.get('reference_number')
    doctor_name = request.form.get('doctor_name')
    print('Doctor name in reschedule_version_two: ', doctor_name)
    form = EditAppointmentForm()
    appointment_data = models_receptionist.Appointment.get_appointment_by_reference_version_two(reference_number)

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
        time_data = models_receptionist.Appointment.get_all_available_schedules(appointment_data['date_appointment'])
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
        if models_receptionist.Appointment.update_second_version(
            reference_number, new_date_appointment, new_time_appointment, new_status_,
            new_last_name, new_email):
            # Update the slots for the old and new times
            models_receptionist.Appointment.update_time_slots(old_date_appointment, new_date_appointment, old_time_appointment, new_time_appointment, doctor_name)

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
            search_results = models_receptionist.Appointment.search_appointment(search_query)
            print("Search results:", search_results)
        else:
            search_results = models_receptionist.Appointment.filter_appointment(filter_by, search_query)
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
        time_schedules = models_receptionist.Appointment.all_time_schedules(selected_date, selected_doctor)
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
        cancel_appointment = models_receptionist.Appointment.get_appointment_by_reference(reference_number)
        cancelled_time = cancel_appointment['time_appointment']

        if models_receptionist.Appointment.update_to_cancel(reference_number, cancel_status):
            # Increment the slots for the deleted time
            models_receptionist.Appointment.update_slots(cancel_appointment['date_appointment'], cancelled_time, doctor_name, increment=True)

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
        appointment_data = models_receptionist.Appointment.get_appointment_by_reference_version_two(reference_number)

        if appointment_data:
            # Fetch time options based on the appointment's date
            date_appointment = appointment_data.get('date_appointment')  # Adjust accordingly
            time_options = models_receptionist.Appointment.get_all_available_schedules(date_appointment)

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
        doctor_id = models_receptionist.Appointment.get_doctor_id(selected_doctor)
        print('Doctor ID', doctor_id)
        return jsonify(success=True, doctor_id=doctor_id)
    except Exception as e:
        return jsonify(success=False, message=str(e))