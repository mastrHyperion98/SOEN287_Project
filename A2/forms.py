from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, PasswordField, SelectField
from wtforms.fields.html5 import EmailField, DateField, IntegerField
from wtforms.validators import InputRequired, Email, Length, Regexp, ValidationError, NumberRange, EqualTo, DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[InputRequired(), Email()])
    password = PasswordField('Password:', validators=[InputRequired()])
    submit = SubmitField('Login')


class CreateAccount(FlaskForm):
    email = EmailField('Email:', validators=[InputRequired(), Email()])
    username = StringField('Username:', validators=[InputRequired(), Length(6,16)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(8, 16)])
    confirm = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Create Account')