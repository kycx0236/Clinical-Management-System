from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class UserForm(FlaskForm):

    # USER INFORMATION
    user_id = StringField("User ID")
    username = StringField("Username", validators=[DataRequired(), Length(max=20)])
    password = StringField("Password", validators=[DataRequired(), Length(max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    middle_name = StringField('Middle Name', validators=[Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    gender = StringField('Gender', validators=[DataRequired(), Length(max=20)])
    user_role = StringField('User Role', validators=[DataRequired(), Length(max=20)])