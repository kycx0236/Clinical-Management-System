from flask import render_template, redirect, request, url_for
from app.forms.doctor_f import *
import app.models as models
from app.models.doctor_m import *
from flask import Blueprint

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/')
def dashboard():
    return render_template("doctor/dashboard.html")

@doctor_bp.route('/calendar/')
def calendar():
    return render_template("doctor/calendar.html")

@doctor_bp.route('/appointment/')
def appointment():
    return render_template("doctor/appointment.html")

@doctor_bp.route('/patient/')
def patient():
    return render_template("doctor/patient.html")

@doctor_bp.route('/profile/')
def profile():
    return render_template("doctor/profile.html")

@doctor_bp.route('/login/')
def logout():
    return render_template("login.html")