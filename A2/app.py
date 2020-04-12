import os
import json
from flask import Flask, render_template, url_for, redirect, request, session, current_app, send_from_directory, \
    send_file
from forms import LoginForm, CreateAccount, Settings
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/db.sqlite3'
app.secret_key = os.environ.get('SECRET_KEY') or 'DEV'
db = SQLAlchemy(app)

from utils import ValidateAccount

@app.route('/')
def index():
    return redirect(url_for("login"))


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for("dashboard"))
    return render_template("Login.html", form=form)


@app.route('/create-account', methods=['POST', 'GET'])
def create_account():
    form = CreateAccount()
    if form.validate_on_submit():
        ValidateAccount(form, db)
        return redirect(url_for("login"))
    return render_template("CreateAccount.html", form=form)


@app.route('/dashboard')
def dashboard():
    channels_str = '''[{"channel_name": "SOEN287", "channel_id": "SOEN287_HYUBN811ALO2"},
     {"channel_name": "COMP371", "channel_id": "COMP371_HYUBN811ALO2"}]'''
    channel = json.loads(channels_str)
    return render_template("Dashboard.html", channels=channel)


@app.route('/settings/account', methods=['POST', 'GET'])
def account_settings():
    form = Settings()

    if form.validate_on_submit():
        return render_template("AccountSettings.html", form=form, username="Hyperion", email="Mastr.hyperion98@gmail.com",
                               permalink="128UA90NV67M")
    return render_template("AccountSettings.html", form=form, username="Hyperion", email="Mastr.hyperion98@gmail.com",
                           permalink="128UA90NV67M")


@app.route('/channels')
def channels():
    json_str = '''[{"user_name": "Hyperion", "permalink": "HYUBN811ALO2", "last_login": "2020-04-15"},
    {"user_name": "Hyperion", "permalink": "HYUBN811ALO2", "last_login": "2020-04-15"},
    {"user_name": "Hyperion", "permalink": "HYUBN811ALO2", "last_login": "2020-04-15"},
    {"user_name": "Hyperion", "permalink": "HYUBN811ALO2", "last_login": "2020-04-15"},
    {"user_name": "Hyperion", "permalink": "HYUBN811ALO2", "last_login": "2020-04-15"}]'''

    channels_str = '''[{"channel_name": "SOEN287", "channel_id": "SOEN287_HYUBN811ALO2"},
    {"channel_name": "COMP371", "channel_id": "COMP371_HYUBN811ALO2"}]'''
    channel = json.loads(channels_str)
    user = json.loads(json_str)
    return render_template("Channels.html", users=user, channels=channel)


@app.route('/download/<string:permalink>')
def download_user_data(permalink):
    path = "Data/" + permalink + ".txt"
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run()
