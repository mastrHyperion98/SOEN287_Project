from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hello world"


@app.route('/login')
def login():
    return render_template("Login.html")


if __name__ == '__main__':
    app.run()
