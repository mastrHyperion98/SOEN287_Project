from flask import Flask, render_template, url_for, redirect, request, session

app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect(url_for("login"))


@app.route('/login')
def login():
    return render_template("Login.html")


@app.route('/create/account')
def create_account():
    return render_template("CreateAccount.html")


@app.route('/login/verify', methods=['POST'])
def verify_login():
    #here we can verify the login credential before redirecting to the dashboard
    #we can also add the user to the session here.
    return redirect(url_for("dashboard"))


@app.route('/dashboard')
def dashboard():
    return render_template("base_home.html")


if __name__ == '__main__':
    app.run()
