from flask_wtf import FlaskForm
from forms import CreateAccount
from model.users import Users


def ValidateAccount(form, db):
    print(form.email.data)
    email = form.email.data
    password = form.password.data
    username = form.username.data
    permalink = "RSQ1T4A1"
    my_user = Users(email=email, password=password, username=username, permalink=permalink)
    db.session.add(my_user)
    db.session.commit()
    print("SUCCSS! User added to Database")
