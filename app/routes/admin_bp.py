from flask import render_template, redirect, request, url_for
from app.forms.admin_f import *
import app.models as models
from app.models.admin_m import *
from flask import Blueprint
from flask_login import login_required, logout_user
from app.routes.utils import role_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
@role_required('admin')
def dashboard():
    return render_template("admin/dashboard.html")

@admin_bp.route('/user_management')
@login_required
@role_required('admin')
def user_management():
    return render_template("admin/user_management.html")

@admin_bp.route('/profile')
@login_required
@role_required('admin')
def profile():
    return render_template("admin/profile.html")

@admin_bp.route("/logout")
@login_required
def logout():
    print("Logout route accessed")  
    logout_user()
    return redirect(url_for('login'))