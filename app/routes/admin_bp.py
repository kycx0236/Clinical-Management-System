from flask import render_template, redirect, request, url_for
from app.forms.admin_f import *
import app.models as models
from app.models.admin_m import *
from flask import Blueprint
from flask_login import login_required, logout_user, current_user
from app.routes.utils import role_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
@role_required('admin')
def dashboard():
    current_id = current_user.id 
    admin_info = admin.get_user(current_id)
    print(admin_info)
    return render_template("admin/dashboard.html", info=admin_info)

@admin_bp.route('/user_management/')
@login_required
@role_required('admin')
def user_management():
    current_id = current_user.id 
    admin_info = admin.get_user(current_id)
    print(admin_info)
    return render_template("admin/user_management.html", info=admin_info)

@admin_bp.route('/profile/')
@login_required
@role_required('admin')
def profile():
    current_id = current_user.id 
    admin_info = admin.get_user(current_id)
    print(admin_info)
    return render_template("admin/profile.html", info=admin_info)

@admin_bp.route("/logout/")
@login_required
def logout():
    print("Logout route accessed")  
    logout_user()
    return redirect(url_for('login'))