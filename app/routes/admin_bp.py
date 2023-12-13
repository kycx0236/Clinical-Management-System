from flask import render_template, redirect, request, url_for, flash
from app.forms.admin_f import *
import app.models as models
from app.models.admin_m import *
from flask import Blueprint
from flask_login import login_required, logout_user
from app.routes.utils import role_required
from werkzeug.security import generate_password_hash


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
# ADD USER
@admin_bp.route('/add_user/', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_user():
    form = UserForm()
    password = admin.generate_password()
    hashed_password = generate_password_hash(password)

    if request.method == 'POST':
        username = form.username.data
        first_name = form.first_name.data
        middle_name = form.middle_name.data
        last_name = form.last_name.data
        email = form.email.data
        gender = form.gender.data
        user_role = form.user_role.data

        new_user = admin()
        new_user.username = username
        new_user.password = hashed_password
        new_user.first_name = first_name
        new_user.middle_name = middle_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.gender = gender
        new_user.user_role = user_role

        if admin.check_existing_user(username) == True:
            return render_template("admin/user_management/add_user.html", error=True, UserForm=form, password=hashed_password)
        
        else: 
            result = new_user.add_user()
            admin.send_message(email,password)
       
        if result:
            return render_template("admin/user_management/add_user.html", success=True, UserForm=form, password=hashed_password)
        else:
            
            return render_template("admin/user_management/add_user.html", error=True, UserForm=form, password=hashed_password)
  
    
    return render_template("admin/user_management/add_user.html", UserForm=form, password=hashed_password)

# DELETE USER
@admin_bp.route('/delete_user/', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def delete_user():
    form = UserForm()

    if request.method == "POST":
        user_id = request.form.get("user_id")

        result = admin.delete_user_record(user_id)

        if result:
            return render_template("admin/user_management/user_management.html", success=True, UserForm=form)
        else:
            return render_template("admin/user_management/user_management.html", error=True, UserForm=form)
        
    return render_template("admin/user_management/user_management.html", UserForm=form)

@admin_bp.route('/user_info/', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def user_info():
    form = UserForm()

    if request.method == 'GET':
        user_id = request.args.get('user_id')
        user_info = admin.get_user_info(user_id)
        
        return render_template('admin/user_management/user_info.html', user=user_info, user_id=user_id, UserForm=form)

    elif request.method == 'POST':
        user_id = request.form.get('user_id')
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        gender = request.form.get('gender')
        user_role = request.form.get('user_role')

        new_password = request.form.get('new_password')  # Add this line

        updated = admin.update_user(user_id, username, password, first_name, middle_name, last_name, gender, user_role, new_password)
        user_info = admin.get_user_info(user_id)

        if updated:
            return render_template('admin/user_management/user_info.html', user=user_info, user_id=user_id, UserForm=form, success=True)
        else:
            return render_template('admin/user_management/user_info.html', user=user_info, user_id=user_id, UserForm=form,error=True)

    return render_template('admin/user_management/user_info.html', user=user_info, user_id=user_id, UserForm=form)