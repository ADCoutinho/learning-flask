# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Log In")


# Form to register user in the system
class RegistrationForm(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Passowrd: ", validators=[
        DataRequired(), EqualTo(
            'pass_confirm', message="Passwords must match!")])
    pass_confirm = PasswordField(
        "Confirm Password: ", validators=[DataRequired()])
    submit = SubmitField("Register!")

    '''
    def check_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError("Your email has been already registered!")

    def check_username(self, username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError("Username already taken!")
    '''
    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError('Email has been registered')
            
    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError('Username has been registered')
