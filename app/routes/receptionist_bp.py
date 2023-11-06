from flask import render_template, redirect, request, url_for, flash
import math
from app.forms.receptionist_f import AppointmentForm
import app.models.receptionist_m as models_receptionist
from flask import Blueprint

receptionist_bp = Blueprint('receptionist', __name__)

headings = ("Reference Number", "Date", "Time", "Status", "Actions")

# Main routes
@receptionist_bp.route('/')
def dashboard():
    return render_template("receptionist/dashboard.html")

@receptionist_bp.route('/calendar/')
def calendar():
    return render_template("receptionist/calendar.html")

@receptionist_bp.route('/appointment/')
def appointment():
    # Get the page number from the query string, default to 1 if not specified
    page = int(request.args.get('page', 1))

    # Set the number of items to display per page
    items_per_page = 5  # You can adjust this to your preferred value

    # Retrieve all appointment data from your model
    all_appointments = models_receptionist.Appointment.all()

    # Calculate the total number of pages
    total_pages = math.ceil(len(all_appointments) / items_per_page)

    # Calculate the starting and ending index for the current page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    # Get the data for the current page
    data = all_appointments[start_index:end_index]

    return render_template("receptionist/appointment.html", headings=headings, data=data, page=page, total_pages=total_pages)


@receptionist_bp.route('/profile/')
def profile():
    return render_template("receptionist/profile.html")

@receptionist_bp.route('/login/')
def logout():
    return render_template("login.html")

# Function routes

@receptionist_bp.route('/add-appointment/', methods=['POST', 'GET'])
def add_appointment():
    form = AppointmentForm(request.form)
    
    if request.method == 'POST' and form.validate():
        check_reference = form.reference_number.data
        reference_exists = models_receptionist.Appointment.unique_code(check_reference)

        if reference_exists:
            flash("Appointment already exists. Please enter a new appointment.")
        
        else:
            new_appointment = models_receptionist.Appointment(
                reference_number=check_reference,
                date_appointment= form.date_appointment.data,
                time_appointment=form.time_appointment.data,
                status_ = form.status_.data,
                book_date = form.book_date.data,
                first_name = form.first_name.data,
                middle_name = form.middle_name.data,
                last_name = form.last_name.data,
                sex = form.sex.data,
                birth_date = form.birth_date.data,
                contact_number = form.contact_number.data,
                email = form.email.data,
                address = form.address.data
            )
            new_appointment.add()
            flash('New appointment added!', 'success')
            return redirect(url_for('receptionist.appointment'))
    
    return render_template("receptionist/appointment_add.html", form=form)


