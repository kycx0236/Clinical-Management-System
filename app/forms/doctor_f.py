from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class PatientForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    midName = StringField('Middle Name', validators=[Length(max=50)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    age = IntegerField('Age', validators=[DataRequired()])
    civilStatus = StringField('Civil Status', validators=[DataRequired(), Length(max=20)])
    gender = StringField('Gender', validators=[DataRequired(), Length(max=10)])
    bloodType = StringField('Blood Type', validators=[Length(max=10)])
    birthPlace = StringField('Birth Place', validators=[Length(max=100)])
    birthDate = DateField('Birth Date (YYYY-MM-DD)', validators=[DataRequired()], format='%Y-%m-%d')
    p_address = StringField('Address', validators=[DataRequired(), Length(max=255)])
    nationality = StringField('Nationality', validators=[Length(max=20)])
    religion = StringField('Religion', validators=[DataRequired(), Length(max=50)])
    eContactName = StringField('Emergency Contact One', validators=[Length(max=20)])
    relationship = StringField('Relationship One', validators=[Length(max=20)])
    eContactNum = StringField('Contact Number One', validators=[Length(max=20)])
    occupation = StringField('Occupation', validators=[Length(max=50)])
    p_email = StringField('Email', validators=[DataRequired(), Length(max=50)])
    p_contactNum = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Submit')
