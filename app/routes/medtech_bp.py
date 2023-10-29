from flask import render_template, redirect, request, url_for
from app.forms.medtech_f import *
import app.models as models
from app.models.medtech_m import *
from flask import Blueprint

medtech_bp = Blueprint('medtech', __name__)

@medtech_bp.route('/')
def dashboard():
    return render_template("medtech/dashboard.html")

@medtech_bp.route('/patient/')
def patient():
    return render_template("medtech/patient.html")

@medtech_bp.route('/profile/')
def profile():
    return render_template("medtech/profile.html")

@medtech_bp.route('/login/')
def logout():
    return render_template("login.html")