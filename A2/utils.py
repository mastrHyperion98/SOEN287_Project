import string
from functools import wraps

import bcrypt
import random
from sqlalchemy.exc import IntegrityError
from model.users import Users
from flask import session, flash, redirect, url_for, request

bcrypt_salt = "$2a$10$ssTHsnejHc6RrlyVbiNQ/O".encode('utf8')


def validate_account(form, db):
    email = form.email.data
    tmp_password = form.password.data
    username = form.username.data
    #randomly generate an 8 character permalink it should be unique
    # create a random sequence of length 16. A mix of letters and digits.
    permalink= ""
    for x in range(16):
        if random.randint(0, 11) <= 5:
            permalink = permalink + random.choice(string.ascii_letters)
        else:
            permalink = permalink + random.choice(string.digits)
    #Add a check to see if permalink is in database and loop until we create a permalink that is not
    #hash the password before storing it inside the database for security concerns
    password = bcrypt.hashpw(tmp_password.encode('utf8'), salt=bcrypt_salt).decode('utf8')
    my_user = Users(email=email, password=password, username=username, permalink=permalink)
    # check if checkpw works
    print(bcrypt.checkpw(tmp_password.encode('utf8'), password.encode('utf8')))
    db.session.add(my_user)
    try:
        db.session.commit()
        return True
    except IntegrityError:
        #cancel all changes
        db.session.rollback()
        return False

# verify login information and add user to session
def verify_login(form, db):
    email = form.email.data
    password = form.password.data
    #check database to see if we find user with given email
    user = Users.query.filter_by(email=email).first()
    if user is None:
        flash(u'Email is not registered to a user!', 'error')
        return False
    elif bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):
        #login_the user
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
    if form.password.data != "":
        password = bcrypt.hashpw(form.password.data.encode('utf8'), salt=bcrypt_salt).decode('utf8')

    #find user in database
    user_id = session['user']["id"]
    user = db.session.query(Users).get(user_id)
    if email:
        user.email = email
        is_email = True
        print("UPDATING EMAIL")
    if password:
        user.password = password
        is_password = True
        print("UPDATING PASSWORD")

    if is_email and is_password:
        flash(u'The password and Email have been updated!', 'info')
        print("SUCCESS! Fields UPDATED")
    elif is_email:
        flash(u'The Email has been updated!', 'info')
    elif is_password:
        flash(u'The password has been updated!', 'info')
    else:
        flash(u'An Error has occurred and the fields cannot be updated', 'error')
        return False

    db.session.commit()
    session['user']=user.to_json()
    return True


def find_user(user_id, db):
    user = Users.query.filter_by(id=user_id).first()
    if user is None:
        return None
    else:
        return user

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            session['next']=request.url
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap
