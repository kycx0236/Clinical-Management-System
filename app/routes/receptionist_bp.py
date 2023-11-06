from flask import render_template, redirect, request, url_for
from app.forms.receptionist_f import *
import app.models as models
from app.models.receptionist_m import *
from flask import Blueprint

receptionist_bp = Blueprint('receptionist', __name__)

@receptionist_bp.route('/')
def dashboard():
    return render_template("receptionist/dashboard.html")

@receptionist_bp.route('/calendar/')
def calendar():
    return render_template("receptionist/calendar.html")

@receptionist_bp.route('/appointment/')
def appointment():
    return render_template("receptionist/appointment.html")

@receptionist_bp.route('/profile/')
def profile():
    return render_template("receptionist/profile.html")

@receptionist_bp.route('/login/')
def logout():
    return render_template("login.html")