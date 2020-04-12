import string
import bcrypt
import random
from sqlalchemy.exc import IntegrityError
from model.users import Users
from flask import session, flash

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
        session['user'] = user.to_json()
        return True
    else:
        flash(u'Password is incorrect!', 'error')
        return False
