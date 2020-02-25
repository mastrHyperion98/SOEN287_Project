from flask import Flask, render_template, url_for, redirect

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

if __name__ == '__main__':
    app.run()
