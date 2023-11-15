from flask import render_template, redirect, request, url_for
from app.forms.medtech_f import *
import app.models as models
from app.models.medtech_m import *
from flask import Blueprint
from flask_login import login_required, logout_user
from app.routes.utils import role_required

medtech_bp = Blueprint('medtech', __name__)

@medtech_bp.route('/')
@login_required
@role_required('medtech')
def dashboard():
    return render_template("medtech/dashboard.html")

@medtech_bp.route('/patient')
@login_required
@role_required('medtech')
def patient():
    return render_template("medtech/patient.html")

@medtech_bp.route('/profile')
@login_required
@role_required('medtech')
def profile():
    return render_template("medtech/profile.html")

@medtech_bp.route('/logout')
@login_required
@role_required('medtech')
def logout():
    logout_user()
    return redirect(url_for('login'))