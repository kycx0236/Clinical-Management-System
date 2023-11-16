from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class PatientForm(FlaskForm):

    # LABORATORY TEST RESULTS
    processName = StringField('Process Name', validators=[DataRequired(), Length(max=255)])
    testResult = StringField('Test Result', validators=[DataRequired(), Length(max=255)])
    refValue = StringField('Reference Value', validators=[DataRequired(), Length(max=255)])
    diagnosisReport = StringField('Diagnosis Report', validators=[DataRequired(), Length(max=255)])
    
    submit = SubmitField('Submit')