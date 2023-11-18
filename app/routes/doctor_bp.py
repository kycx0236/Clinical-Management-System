from flask import render_template, redirect, request, url_for
from app.forms.doctor_f import *
import app.models as models
from app.models.doctor_m import *
from flask import Blueprint
from flask_login import login_required, logout_user
from app.routes.utils import role_required

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/')
@login_required
@role_required('doctor')
def dashboard():
    return render_template("doctor/dashboard.html")

@doctor_bp.route('/calendar')
@login_required
@role_required('doctor')
def calendar():
    return render_template("doctor/calendar.html")

@doctor_bp.route('/appointment')
@login_required
@role_required('doctor')
def appointment():
    return render_template("doctor/appointment.html")

@doctor_bp.route('/patient')
@login_required
@role_required('doctor')
def patient():
    return render_template("doctor/patient.html")

@doctor_bp.route('/profile')
@login_required
@role_required('doctor')
def profile():
    return render_template("doctor/profile.html")

@doctor_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))