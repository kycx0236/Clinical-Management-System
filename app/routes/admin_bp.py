from flask import render_template, redirect, request, url_for, flash
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
    users_data = admin.get_users()
    print(admin_info)
    return render_template("admin/user_management/user_management.html", info=admin_info, users=users_data)

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

# -------------------------------------------- USER -------------------------------------------- #
# ADD USER
@admin_bp.route('/add_user/',  methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_user():
    form = UserForm()
    current_id = current_user.id 
    admin_info = admin.get_user(current_id)

    if request.method == 'POST':
        admin_info = admin.get_user(current_id)
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        middle_name = form.middle_name.data
        last_name = form.last_name.data
        gender = form.gender.data
        user_role = form.user_role.data

        new_user = admin()
        new_user.username = username
        new_user.password = password
        new_user.first_name = first_name
        new_user.middle_name = middle_name
        new_user.last_name = last_name
        new_user.gender = gender
        new_user.user_role = user_role

        result = new_user.add_user()

        if result:
            return render_template("admin/user_management/add_user.html", success=True, UserForm=form, info=admin_info)
        else:
            return render_template("admin/user_management/add_user.html", error=True, UserForm=form, info=admin_info)
    
    return render_template("admin/user_management/add_user.html", UserForm=form, info=admin_info)

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

        updated = admin.update_user(user_id, username, password, first_name, middle_name, last_name, gender, user_role)
        user_info = admin.get_user_info(user_id)

        if updated:
            return render_template('admin/user_management/user_info.html', user=user_info, user_id=user_id, UserForm=form, success=True)
        else:
            return render_template('admin/user_management/user_info.html', user=user_info, user_id=user_id, UserForm=form,error=True)

    return render_template('admin/user_management/user_info.html', user=user_info, user_id=user_id, UserForm=form)