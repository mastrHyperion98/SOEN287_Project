import string
from functools import wraps

import bcrypt
import random
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from model.users import Users
from flask import session, flash, redirect, url_for

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
        print("SUCCSS! User added to Database")
        return True
    except IntegrityError:
        #cancel all changes
        db.session.rollback()
        print("Integrity ERROR!")
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
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap
