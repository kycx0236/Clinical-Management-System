from flask import render_template, redirect, request, url_for
# from ssis_app.college.forms import *
# import ssis_app.models as models
# from ssis_app.models.college import *
from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def dashboard():
    return render_template("admin.html")

@admin_bp.route('/user_management/')
def user_management():
    return render_template("admin_user_management.html")

@admin_bp.route('/profile/')
def profile():
    return render_template("admin_profile.html")

@admin_bp.route('/login/')
def logout():
    return render_template("login.html")