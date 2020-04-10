import os
import json
from flask import Flask, render_template, url_for, redirect, request, session, current_app, send_from_directory, \
    send_file

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for("login"))


@app.route('/login')
def login():
    return render_template("Login.html")


@app.route('/create/account')
def create_account():
    return render_template("CreateAccount.html")


@app.route('/createAccount/verify', methods=['POST', 'GET'])
def verify_createAccount():
    return redirect(url_for("login"))


@app.route('/login/verify', methods=['POST', 'GET'])
def verify_login():
    #here we can verify the login credential before redirecting to the dashboard
    #we can also add the user to the session here.
    return redirect(url_for("dashboard"))


@app.route('/dashboard')
def dashboard():
    channels_str = '''[{"channel_name": "SOEN287", "channel_id": "SOEN287_HYUBN811ALO2"},
     {"channel_name": "COMP371", "channel_id": "COMP371_HYUBN811ALO2"}]'''
    channel = json.loads(channels_str)
    return render_template("Dashboard.html", channels=channel)


@app.route('/settings/account')
def account_settings():
    return render_template("AccountSettings.html", username="Hyperion", email="Mastr.hyperion98@gmail.com", permalink="128UA90NV67M")


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
    return render_template("Channels.html", users = user, channels= channel)


@app.route('/download/<string:permalink>')
def download_user_data(permalink):
	path = "Data/" +permalink + ".txt"
	return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run()
