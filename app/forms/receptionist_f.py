from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, DateField, SelectField, EmailField, IntegerField

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


