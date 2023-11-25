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

@admin_bp.route('/user_management/')
@login_required
@role_required('admin')
def user_management():
    users_data = admin.get_users()
    return render_template("admin/user_management/user_management.html", users=users_data)

@admin_bp.route('/profile/')
@login_required
@role_required('admin')
def profile():
    return render_template("admin/profile.html")

@admin_bp.route("/logout/")
@login_required
def logout():
    print("Logout route accessed")  
    logout_user()
    return redirect(url_for('login'))

# -------------------------------------------- USER -------------------------------------------- #

@admin_bp.route('/add_user/',  methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_user():
    form = UserForm() 
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        firstname = request.form.get("first_name").upper()
        middlename = request.form.get("middle_name").upper()
        lastname = request.form.get("last_name")
        gender = request.form.get("gender")
        userrole = request.form.get("user_role").upper()
        
        
        
        return redirect(url_for('admin.user_management'))
    return render_template("admin/user_management/add_user.html", UserForm=form)