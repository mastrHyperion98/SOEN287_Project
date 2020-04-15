import string
from datetime import datetime, date
from functools import wraps

import bcrypt
import random
from sqlalchemy.exc import IntegrityError
from model.users import Users
from model.channels import Channels
from model.members import Members
from flask import session, flash, redirect, url_for, request, json
from flask_mail import Mail, Message

bcrypt_salt = "$2a$10$ssTHsnejHc6RrlyVbiNQ/O".encode('utf8')


def validate_account(form, db):
    email = form.email.data
    tmp_password = form.password.data
    username = form.username.data
    # randomly generate an 8 character permalink it should be unique
    # create a random sequence of length 16. A mix of letters and digits.
    permalink = ""
    for x in range(16):
        if random.randint(0, 11) <= 5:
            permalink = permalink + random.choice(string.ascii_letters)
        else:
            permalink = permalink + random.choice(string.digits)
    # Add a check to see if permalink is in database and loop until we create a permalink that is not
    # hash the password before storing it inside the database for security concerns
    password = bcrypt.hashpw(tmp_password.encode('utf8'), salt=bcrypt_salt).decode('utf8')
    my_user = Users(email=email, password=password, username=username, permalink=permalink)
    # check if checkpw works
    print(bcrypt.checkpw(tmp_password.encode('utf8'), password.encode('utf8')))
    db.session.add(my_user)
    try:
        db.session.commit()
        return True
    except IntegrityError:
        # cancel all changes
        db.session.rollback()
        return False


# verify login information and add user to session
def verify_login(form, db):
    email = form.email.data
    password = form.password.data
    # check database to see if we find user with given email
    user = db.session.query(Users).filter_by(email=email).first()
    if user is None:
        flash(u'Email is not registered to a user!', 'error')
        return False
    elif bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):
        # login_the user
        user.login = datetime.now()
        db.session.commit()
        session['user'] = user.to_json()
        return True
    else:
        flash(u'Password is incorrect!', 'error')
        return False


def update_user(form, db):
    is_email = False
    is_password = False
    email = ""
    password = ""
    if form.email.data != "":
        email = form.email.data
        # check if email already exists in the database
        tmp_user = Users.query.filter_by(email=email).first()
        if tmp_user is not None:
            flash(u'This email is already in use!', 'error')
            return False
    if form.password.data != "":
        password = bcrypt.hashpw(form.password.data.encode('utf8'), salt=bcrypt_salt).decode('utf8')

    # find user in database
    user_id = session['user']["id"]
    user = db.session.query(Users).get(user_id)
    if email:
        user.email = email
        is_email = True
    if password:
        user.password = password
        is_password = True

    if is_email and is_password:
        flash(u'The password and Email have been updated!', 'info')
        session['user']['email'] = email
    elif is_email:
        flash(u'The Email has been updated!', 'info')
        session['user']['email'] = email
    elif is_password:
        flash(u'The password has been updated!', 'info')
    else:
        flash(u'An Error has occurred and the fields cannot be updated', 'error')
        return False

    db.session.commit()
    return True


def add_channel(form, db):
    name = form.name.data
    admin_id = session['user']['id']
    permalink = ""

    while True:  # generate a permalink not in the database same algo as for user
        for x in range(16):
            if random.randint(0, 11) <= 5:
                permalink = permalink + random.choice(string.ascii_letters)
            else:
                permalink = permalink + random.choice(string.digits)
            tmp_channel = Channels.query.filter_by(permalink=permalink).first()
            # if none then safe to add
        if tmp_channel is None:
            break
    # check for duplicate name for given admin_id
    user = Users.query.filter_by(id=admin_id).first()
    channels = user.channels

    for channel in channels:
        if channel.name == name:
            flash(u'You already have a channel with this name!', 'error')
            return False

    channel = Channels(admin_id=admin_id, name=name, permalink=permalink)
    db.session.add(channel)
    try:
        db.session.commit()
        channel = Channels.query.filter_by(name=name, admin_id=admin_id).first()
        member = Members(channel_id=channel.id, user_id=admin_id, is_admin=True)
        db.session.add(member)
        db.session.commit()
        flash(u'' + name + " has been created!", 'info')
        return True
    except IntegrityError:
        # cancel all changes
        flash(u'Inputs are empty!', 'error')
        db.session.rollback()
        return False


def find_user(user_id, db):
    user = Users.query.filter_by(id=user_id).first()
    if user is None:
        return None
    else:
        return user


def my_channels(db):
    user_id = session['user']['id']
    user = Users.query.filter_by(id=user_id).first()
    channels = user.channels
    list = []
    for channel in channels:
        list.append(channel.to_json())
    # else no channels exists
    return json.dumps(list)


def member_of(db):
    # Query for our user
    user = Users.query.filter_by(permalink=session['user']['permalink']).first()
    # fetch the list of membership
    member_of = user.channel_member

    list = []
    for channel in member_of:
        channel_member = Channels.query.filter_by(id=channel.channel_id).first()
        list.append(channel_member.to_json())

    return json.dumps(list)


def get_channel_members(db,permalink):
    # fetch our channel from the databas
    channel = Channels.query.filter_by(permalink=permalink).first()
    # next get the members of the channel
    # check if we have the authority to look!
    if channel is None or session['user']['id'] != channel.admin_id:
        return json.dumps([])

    list_of_members = channel.members

    list = []
    for members in list_of_members:
        user = db.session.query(Users).filter_by(id=members.user_id).first()
        if user is not None:
            entry = user.to_json()
            entry['is_admin'] = members.is_admin
            list.append(entry)
    # return the list of members
    return json.dumps(list)


def recover_password(form, mail, db):
    email = form.email.data
    # fetch user with given email
    user = db.session.query(Users).filter_by(email=email).first()
    if user is None:
        flash(u'This email is not associated to any users!', 'error')
        return False

    # generate a 16 string password
    tmp_password = ""
    for x in range(16):
        if random.randint(0, 11) <= 5:
            tmp_password = tmp_password + random.choice(string.ascii_letters)
        else:
            tmp_password = tmp_password + random.choice(string.digits)
    # encrypt the password
    password = bcrypt.hashpw(tmp_password.encode('utf8'), salt=bcrypt_salt).decode('utf8')
    # Update the password in the database
    user.password = password
    db.session.commit()

    print(tmp_password + "HAS BEEN RESET")

    msg = Message('Chatty Password Reset!', recipients=[email])
    msg.html = '<body><h2> Chatty Password Reset Request!</h2><hr/> Hi ' + user.username + \
               ', following your password reset request our team has reset the password of your account. You can use' \
               ' the temporary password below to login into your account and change your password. ' \
               'Thank you for placing your trust in Chatty<br><br>Temporary Password: ' + tmp_password + '</body>'
    mail.send(msg)
    print("Email SENT!")
    flash(u'An email has been sent to you!', 'info')
    return True


def deleteChannel(db, permalink):
    channel = db.session.query(Channels).filter_by(permalink=permalink).first()
    if channel is None:
        return False

    # we also need to remove all members therefore
    members = channel.members

    for member in members:
        db.session.delete(member)

    db.session.delete(channel)
    db.session.commit()
    return True


def remove_member(db):
    user_permalink = request.json['permalink']
    channel_permalink = request.json['channel']
    channel = db.session.query(Channels).filter_by(permalink=channel_permalink).first()
    members = channel.members
    user_id = Users.query.filter_by(permalink=user_permalink).first().id

    for member in members:
        # print(member.user_id)
        if member.user_id == user_id:
            db.session.delete(member)
            db.session.commit()
            return True

    return False


def add_member(form, db):
    user = Users.query.filter_by(permalink=form.permalink.data).first()
    if user is None:
        flash(u'This user does not exist!', 'error')
        return False

    ch_permalink=form.channel_permalink.data
    channel = Channels.query.filter_by(permalink=ch_permalink).first()
    channel_id = channel.id

    if channel is None:
        flash(u'You currently do not own any channels', 'error')
        return False

    member = Members(channel_id=channel_id, user_id=user.id)
    members = channel.members

    for people in members:
        if people.user_id == user.id:
            flash(u'This user is already a member of ' + channel.name, 'error')
            return False

    db.session.add(member)
    try:
        db.session.commit()
        flash(u"" + user.username + ' Has been added to ' + channel.name, 'info')
        return True
    except IntegrityError:
        # cancel all changes
        flash(u'This user does not exist!', 'error')
        db.session.rollback()
        return False


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            session['next'] = request.url
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap
