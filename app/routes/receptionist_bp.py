from flask import render_template, redirect, request, url_for
from app.forms.receptionist_f import AppointmentForm
import app.models.receptionist_m as models_receptionist
from flask import Blueprint

receptionist_bp = Blueprint('receptionist', __name__)

headings = ("Reference Number", "Date", "Time", "Status", "Actions")

@receptionist_bp.route('/')
def dashboard():
    return render_template("receptionist/dashboard.html")

@receptionist_bp.route('/calendar/')
def calendar():
    return render_template("receptionist/calendar.html")

@receptionist_bp.route('/appointment/')
def appointment():
    data = models_receptionist.Appointment.all()
    return render_template("receptionist/appointment.html", headings=headings, data=data)

@receptionist_bp.route('/profile/')
def profile():
    return render_template("receptionist/profile.html")

@receptionist_bp.route('/login/')
def logout():
    return render_template("login.html")