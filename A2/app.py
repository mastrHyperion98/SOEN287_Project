import gc
import os
import json
from flask import Flask, render_template, url_for, redirect, request, session, current_app, send_from_directory, \
    send_file, flash
from forms import LoginForm, CreateAccount, Settings, CreateChannelForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/db.sqlite3'
app.secret_key = os.environ.get('SECRET_KEY') or 'DEV'
db = SQLAlchemy(app)
from utils import validate_account, verify_login,find_user,login_required, update_user, add_channel, my_channels, member_of


@app.route('/')
def index():
    return redirect(url_for("login"))


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if verify_login(form, db):
            next_page = session.get('next', url_for("dashboard"))
            session['next']=url_for("dashboard")
            return redirect(next_page)
    return render_template("Login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash(u"You have been logged out!", "info")
    gc.collect()
    return redirect(url_for('login'))

@app.route('/create-account', methods=['POST', 'GET'])
def create_account():
    form = CreateAccount()
    if form.validate_on_submit():
        if validate_account(form, db):
            return redirect(url_for("login"))
        else:
            flash(u'Username or Email already in use', 'error')
    return render_template("CreateAccount.html", form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    channels_str = '''[{"channel_name": "SOEN287", "channel_id": "SOEN287_HYUBN811ALO2"},
     {"channel_name": "COMP371", "channel_id": "COMP371_HYUBN811ALO2"}]'''
    channel = json.loads(member_of(db))
    return render_template("Dashboard.html", channels=channel)


@app.route('/settings/account', methods=['POST', 'GET'])
@login_required
def account_settings():
    user = session['user']
    form = Settings()

    if form.validate_on_submit():
        if update_user(form, db):
            return render_template("AccountSettings.html", form=form, username=user['username'],
                                email=user['email'],
                                permalink=user['permalink'])
    return render_template("AccountSettings.html", form=form, username=user['username'], email=user['email'],
                           permalink=user['permalink'])


@app.route('/channels', methods=['POST', 'GET'])
@login_required
def channels():
    json_str = '''[{"user_name": "Hyperion", "permalink": "HYUBN811ALO2", "last_login": "2020-04-15"},
    {"user_name": "Hyperion", "permalink": "HYUBN811ALO2", "last_login": "2020-04-15"},
    {"user_name": "Hyperion", "permalink": "HYUBN811ALO2", "last_login": "2020-04-15"},
    {"user_name": "Hyperion", "permalink": "HYUBN811ALO2", "last_login": "2020-04-15"},
    {"user_name": "Hyperion", "permalink": "HYUBN811ALO2", "last_login": "2020-04-15"}]'''

    create_channel_form = CreateChannelForm()
    if create_channel_form.validate_on_submit():
        if add_channel(create_channel_form, db):
            channel = json.loads(my_channels(db))
            user = json.loads(json_str)
            return render_template("Channels.html", users=user, channels=channel, add_chanel_form=create_channel_form)
    channel = json.loads(my_channels(db))
    user = json.loads(json_str)
    return render_template("Channels.html", users=user, channels=channel, add_chanel_form = create_channel_form)


@app.route('/download/<string:permalink>')
@login_required
def download_user_data(permalink):
    path = "Data/" + permalink + ".txt"
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run()
