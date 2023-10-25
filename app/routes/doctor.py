from flask import render_template, redirect, request, url_for
# from ssis_app.college.forms import *
# import ssis_app.models as models
# from ssis_app.models.college import *
from flask import Blueprint

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/')
def dashboard():
    return render_template("doctor.html")

@doctor_bp.route('/calendar/')
def calendar():
    return render_template("doctor_calendar.html")

@doctor_bp.route('/appointment/')
def appointment():
    return render_template("doctor_appointment.html")

@doctor_bp.route('/patient/')
def patient():
    return render_template("doctor_patient.html")

@doctor_bp.route('/profile/')
def profile():
    return render_template("doctor_profile.html")

@doctor_bp.route('/login/')
def logout():
    return render_template("login.html")