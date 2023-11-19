from flask import render_template, redirect, request, url_for
from app.forms.receptionist_f import *
import app.models as models
from app.models.receptionist_m import *
from flask import Blueprint
from flask_login import login_required, logout_user
from app.routes.utils import role_required

receptionist_bp = Blueprint('receptionist', __name__)

@receptionist_bp.route('/')
@login_required
@role_required('receptionist')
def dashboard():
    return render_template("receptionist/dashboard.html")

@receptionist_bp.route('/calendar/')
@login_required
@role_required('receptionist')
def calendar():
    return render_template("receptionist/calendar.html")

@receptionist_bp.route('/appointment/')
@login_required
@role_required('receptionist')
def appointment():
    return render_template("receptionist/appointment.html")

@receptionist_bp.route('/profile/')
@login_required
@role_required('receptionist')
def profile():
    return render_template("receptionist/profile.html")

@receptionist_bp.route('/logout/')
@login_required
def logout():
    print("Logout route accessed")  
    logout_user()
    return redirect(url_for('login'))