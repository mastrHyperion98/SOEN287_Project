from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/dashboard')
def dashboard():
    return 'DASHBOARD'

@app.route('/usr/settings-<string:user>')
def user_settings(user):
    return user

if __name__ == '__main__':
    app.run()
