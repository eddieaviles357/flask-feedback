from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    """ Register For User """
    username = StringField("Username", validators=[
                       InputRequired(message="Please Enter a Username"), Length(max=20)])

    password = PasswordField("Password", validators=[
                          InputRequired(message="Please Enter a Password")])

    email = StringField("Email", validators=[ InputRequired(message="Please Enter an Email"), Length(max=50)])

    first_name = StringField("First Name", validators=[ InputRequired(message="Please Enter a First Name"), Length(max=30)])

    last_name = StringField("Last Name", validators=[ InputRequired(message="Please Enter a First Name"), Length(max=30)])

class LoginForm(FlaskForm):
    """ Loging form """
    username = StringField("Username", validators=[
                       InputRequired(message="Please Enter a Username"), Length(max=20)])

    password = PasswordField("Password", validators=[
                          InputRequired(message="Please Enter a Password")])