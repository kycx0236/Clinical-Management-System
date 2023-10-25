from flask import render_template, redirect, request, url_for
# from ssis_app.college.forms import *
# import ssis_app.models as models
# from ssis_app.models.college import *
from flask import Blueprint

medtech_bp = Blueprint('medtech', __name__)

@medtech_bp.route('/')
def dashboard():
    return render_template("medtech.html")

@medtech_bp.route('/patient/')
def patient():
    return render_template("medtech_patient.html")

@medtech_bp.route('/profile/')
def profile():
    return render_template("medtech_profile.html")

@medtech_bp.route('/login/')
def logout():
    return render_template("login.html")