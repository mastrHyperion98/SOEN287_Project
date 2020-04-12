from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, PasswordField, SelectField
from wtforms.fields.html5 import EmailField, DateField, IntegerField
from wtforms.validators import InputRequired, Email, Length, Regexp, ValidationError, NumberRange, EqualTo, DataRequired, Optional


class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[InputRequired(), Email()])
    password = PasswordField('Password:', validators=[InputRequired()])
    submit = SubmitField('Login')


class CreateAccount(FlaskForm):
    email = EmailField('Email:', validators=[InputRequired(), Email()])
    username = StringField('Username:', validators=[InputRequired(), Length(4,16)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(8, 16)])
    confirm = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Create Account')


class Settings(FlaskForm):
    email = EmailField('Email:', validators=[Optional(), Email()])
    username = StringField('Username:', render_kw={'readonly': True})
    password = PasswordField('Password:', validators=[Optional(), Length(8, 16)])
    permalink = StringField('Permalink:', render_kw={'readonly': True})
    submit = SubmitField('Apply Changes')


class CreateChannelForm(FlaskForm):
    name = StringField('Channel Name:', validators=[InputRequired(), Length(4,16)])
    submit = SubmitField("Create Channel")