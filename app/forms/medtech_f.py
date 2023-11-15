from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class PatientForm(FlaskForm):
    orderID = IntegerField('Order ID', validators=[DataRequired()])
    patientID = IntegerField('Patient ID')
    patientName = StringField('Patient Name', validators=[DataRequired(), Length(max=255)])
    gender = StringField('Gender', validators=[DataRequired(), Length(max=10)])
    age = StringField('Age', validators=[DataRequired(), Length(max=10)])
    physician = StringField('Physician', validators=[DataRequired(), Length(max=255)])
    orderDate = StringField('Order Date', validators=[DataRequired(), Length(max=20)])
    otherTest = StringField('Other Test', validators=[Length(max=255)])
    
    submit = SubmitField('Submit')