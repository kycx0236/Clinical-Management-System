from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, DateField


class AppointmentForm(FlaskForm):
    reference_number = StringField('reference_number', [validators.DataRequired(), validators.Length(min=5, max=20)])
    date_appointment = DateField('date_appointment', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    time_appointment = StringField('time_appointment', [validators.Length(min=4, max=50)])
    status_ = StringField('status_', [validators.Length(min=4, max=50)])
    book_date = StringField('book_date', [validators.Length(min=4, max=50)])
    first_name = StringField('first_name', [validators.Length(min=2, max=50)])
    middle_name = StringField('middle_name', [validators.Length(min=2, max=50)])
    last_name = StringField('last_name', [validators.Length(min=2, max=50)])
    sex = StringField('sex', [validators.Length(max=1)])
    birth_date = StringField('birth_date', [validators.Length(min=8, max=50)])
    contact_number = StringField('contact_number', [validators.Length(min=11, max=50)])
    email = StringField('email', [validators.Length(min=10, max=50)])
    address = StringField('address', [validators.Length(min=10, max=50)])
    submit = SubmitField("Submit")

