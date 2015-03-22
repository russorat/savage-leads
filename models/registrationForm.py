from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired

class RegistrationForm(Form):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
