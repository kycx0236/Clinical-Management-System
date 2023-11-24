from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField, BooleanField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length

class UserForm(FlaskForm):

    # User Information
    username = StringField("Username", validators=[DataRequired(), Length(max=20)])
    password = StringField("Password", validators=[DataRequired(), Length(max=20)])
    firstName = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    midName = StringField('Middle Name', validators=[Length(max=50)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    gender = StringField('Gender', validators=[DataRequired(), Length(max=20)])
    user_role = StringField('User Role', validators=[DataRequired(), Length(max=20)])