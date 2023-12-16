from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, DateField, SelectField, EmailField, IntegerField, BooleanField, TextAreaField, DateTimeField, TimeField
from wtforms.validators import DataRequired, Length
from datetime import datetime, timedelta
class AppointmentForm(FlaskForm):
    reference_number = StringField('reference_number', [validators.DataRequired()])
    doctorID = IntegerField('doctorID', [validators.DataRequired()])
    doctorName = StringField('doctorName', [validators.DataRequired()])
    date_appointment = DateField('date_appointment', format='%Y-%m-%d', validators=[validators.InputRequired()])
    time_appointment = StringField('time_appointment', [validators.Length(min=1, max=50)])
    status_ = StringField('status_', [validators.Length(min=4, max=50)])
    first_name = StringField('first_name', [validators.Length(min=2, max=50)])
    middle_name = StringField('middle_name', [validators.Length(min=2, max=50)])
    last_name = StringField('last_name', [validators.Length(min=2, max=50)])
    sex = StringField('sex', [validators.Length(min=3)])
    birth_date = DateField('birth_date', format='%Y-%m-%d', validators=[validators.InputRequired()])
    contact_number = StringField('contact_number', [validators.Length(max=11)])
    email = StringField('email', [validators.Length(min=10, max=50)])
    address = StringField('address', [validators.Length(min=10, max=255)])
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    searchTerm = StringField('Search Term')
    filterBy = SelectField('Filter By', choices=[('all', 'All'), ('reference_number', 'Reference Number'),
                                                 ('date_appointment', 'Date'), ('time_appointment', 'Time'),
                                                 ('last_name', 'Last Name'), ('status_', 'Status')])

class EditAppointmentForm(FlaskForm):
    reference_number = StringField('reference_number', [validators.DataRequired()])
    date_appointment = DateField('date_appointment', format='%Y-%m-%d', validators=[validators.InputRequired()])
    time_appointment = StringField('time_appointment', [validators.Length(min=1, max=50)])
    status_ = StringField('status_', [validators.Length(min=4, max=50)])
    last_name = StringField('last_name', [validators.Length(min=2, max=50)])
    email = EmailField('email', [validators.Length(min=10, max=50)])
    submit = SubmitField("Submit")


class PatientForm(FlaskForm):

    # PATIENT INFORMATION
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    middle_name = StringField('Middle Name', validators=[Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    age = IntegerField('Age', validators=[DataRequired()])
    civil_status = StringField('Civil Status', validators=[DataRequired(), Length(max=20)])
    gender = StringField('Gender', validators=[DataRequired(), Length(max=10)])
    bloodType = StringField('Blood Type', validators=[Length(max=10)])
    birth_place = StringField('Birth Place', validators=[Length(max=100)])
    birth_date = DateField('Birth Date (YYYY-MM-DD)', validators=[DataRequired()], format='%Y-%m-%d')
    p_address = StringField('Address', validators=[DataRequired(), Length(max=255)])
    nationality = StringField('Nationality', validators=[Length(max=20)])
    religion = StringField('Religion', validators=[DataRequired(), Length(max=50)])
    e_person = StringField('Emergency Contact', validators=[Length(max=20)])
    relationship = StringField('Relationship', validators=[Length(max=20)])
    e_number = StringField('Contact Number', validators=[Length(max=20)])
    occupation = StringField('Occupation', validators=[Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Length(max=50)])
    contact_num = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])

    submit = SubmitField('Submit')
    
class ScheduleForm(FlaskForm):
    date_appointment = DateField('date_appointment', format='%Y-%m-%d', validators=[validators.InputRequired()])
    time_appointment = StringField('time_appointment', [validators.Length(min=1, max=50)])
    slots = IntegerField('slots', [validators.DataRequired()])
    doctorID = IntegerField('doctorID', [validators.DataRequired()])
    doctorName = StringField('doctorName', [validators.DataRequired()])
    receptionistID = IntegerField('doctorID', [validators.DataRequired()])