from flask import render_template, redirect, request, url_for
# from ssis_app.college.forms import *
# import ssis_app.models as models
# from ssis_app.models.college import *
from flask import Blueprint

receptionist_bp = Blueprint('receptionist', __name__)

@receptionist_bp.route('/')
def dashboard():
    return render_template("receptionist.html")

@receptionist_bp.route('/calendar/')
def calendar():
    return render_template("receptionist_calendar.html")

@receptionist_bp.route('/appointment/')
def appointment():
    return render_template("receptionist_appointment.html")

@receptionist_bp.route('/profile/')
def profile():
    return render_template("receptionist_profile.html")

@receptionist_bp.route('/login/')
def logout():
    return render_template("login.html")