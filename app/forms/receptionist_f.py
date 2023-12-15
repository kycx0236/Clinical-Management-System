from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField, BooleanField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length

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