from flask import render_template, redirect, request, url_for, flash, jsonify, session
import math
from app.forms.receptionist_f import AppointmentForm
import app.models.receptionist_m as models_receptionist
from flask import Blueprint
from datetime import datetime
import secrets
import string
from flask_login import login_required, logout_user
from app.routes.utils import role_required

receptionist_bp = Blueprint('receptionist', __name__)

headings = ("Reference Number", "Date", "Time", "Status", "Actions")

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
    # Get the page number from the query string, default to 1 if not specified
    page = int(request.args.get('page', 1))

    # Set the number of items to display per page
    items_per_page = 8  # You can adjust this to your preferred value

    # Retrieve all appointment data from your model
    all_appointments = models_receptionist.Appointment.all()

    # Calculate the total number of pages
    total_pages = math.ceil(len(all_appointments) / items_per_page)

    # Calculate the starting and ending index for the current page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    # Get the data for the current page
    data = all_appointments[start_index:end_index]

    return render_template("receptionist/appointment/appointment.html", headings=headings, data=data, page=page, total_pages=total_pages)


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
    # return redirect(url_for('login'))

# Function and function routes

def generate_reference_number():
    characters = string.ascii_uppercase + string.digits
    reference_number = ''.join(secrets.choice(characters) for _ in range(6))
    return reference_number

def generate_status():
    return 'PENDING'

def generate_bookdate():
    current_datetime = datetime.now()
    return current_datetime

@receptionist_bp.route('/add-appointment/', methods=['GET', 'POST'])
def add_appointment():
    form = AppointmentForm(request.form)
    booking_details = None

    if request.method == 'POST':
        try:
            check_reference = generate_reference_number()
            form.reference_number.data = check_reference 
            initial_status = generate_status()
            form.status_.data = initial_status 
            generated_bookdate = generate_bookdate().strftime("%Y-%m-%d %I:%M:%S %p")
            form.book_date.data = generated_bookdate
            
            input_time = request.form['time_appointment']
            time_object = datetime.strptime(input_time, "%H:%M")
            form.time_appointment.data = time_object.strftime("%I:%M %p")
        
            print(request.form)  # Print the form data for debugging
            if form.validate_on_submit():
                reference_exists = models_receptionist.Appointment.unique_code(check_reference)
                
                if reference_exists:
                    flash("Appointment already exists. Please enter a new appointment.")
                else:
                    new_appointment = models_receptionist.Appointment(
                        reference_number=form.reference_number.data,
                        date_appointment=form.date_appointment.data,
                        time_appointment=form.time_appointment.data,
                        status_=form.status_.data,
                        book_date=form.book_date.data,
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
            return jsonify(success=False, message="Internal Server Error"), 500

    return render_template("receptionist/appointment/appointment_add.html", form=form, booking_details=booking_details)

@receptionist_bp.route('/delete-appointment/', methods=['POST'])
def delete_appointment():
    try:
        reference_number = request.form.get('reference_number')
        if models_receptionist.Appointment.delete(reference_number):
            return jsonify(success=True, message="Successfully deleted")
        else:
            return jsonify(success=False, message="Failed to delete appointment")
    except Exception as e:
        # Log the error for debugging purposes
        receptionist_bp.logger.error("An error occurred: %s" % str(e))
        return jsonify(success=False, message="Internal Server Error"), 500


@receptionist_bp.route('/view-appointment/')
def view_appointment():
    try:
        pass
    except:
        pass    

@receptionist_bp.route('/get-booking-details/<reference_number>', methods=['GET'])
def get_booking_details(reference_number):
    booking_details = models_receptionist.Appointment.get_booking_reference_details(reference_number)

    if booking_details:
        return jsonify(booking_details)
    else:
        return jsonify({'error': 'Booking details not available'}), 404
    