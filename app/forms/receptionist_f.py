from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField


class AppointmentForm(FlaskForm):
    reference_number = StringField('reference_number', [validators.DataRequired(), validators.Length(min=5, max=20)])
    date_appointment = StringField('date_appointment', [validators.Length(min=8, max=50)])
    time_appointment = StringField('time_appointment', [validators.Length(min=6, max=50)])
    status_ = StringField('status_', [validators.Length(min=4, max=50)])
    book_date = StringField('book_date', [validators.Length(min=8, max=50)])
    patient_name = StringField('patient_name', [validators.Length(min=8, max=50)])
    birthdate = StringField('birthdate', [validators.Length(min=8, max=50)])
    contact_number = StringField('contact_number', [validators.Length(min=11, max=50)])
    email = StringField('email', [validators.Length(min=10, max=50)])
    submit = SubmitField("Submit")
