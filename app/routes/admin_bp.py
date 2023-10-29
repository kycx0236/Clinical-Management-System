from flask import render_template, redirect, request, url_for
from app.forms.admin_f import *
import app.models as models
from app.models.admin_m import *
from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def dashboard():
    return render_template("admin/dashboard.html")

@admin_bp.route('/user_management/')
def user_management():
    return render_template("admin/user_management.html")

@admin_bp.route('/profile/')
def profile():
    return render_template("admin/profile.html")

@admin_bp.route('/login/')
def logout():
    return render_template("login.html")