import os.path
import pickle

from flask import Flask, url_for
from markupsafe import escape

app = Flask(__name__)

USER_FILE = 'C:\\user_info.data'

if os.path.isfile('C:\\user_info.data'):
    f = open(USER_FILE, 'rb')
    user_info = pickle.load(f)
    f.close()


@app.route('/')
def index():
    return 'index'


@app.route('/login')
def login():
    return 'login'


@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'


with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

if __name__ == "__main__":
    app.run()
