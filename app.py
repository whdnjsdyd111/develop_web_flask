import os.path
import pickle

from flask import Flask, url_for, render_template, request, abort, redirect, session

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
USER_FILE = 'C:\\user_info.data'

if os.path.isfile('C:\\user_info.data'):
    f = open(USER_FILE, 'rb')
    user_info = pickle.load(f)
    f.close()


@app.route('/')
@app.route('/index')
def index():
    return 'main'


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        # if valid_login(request.form['username'],
        #                request.form['password']):
        #     return log_the_user_in(request.form['username'])
        # else:
        #     error = 'Invalid username/password'
        if request.form['id'] in user_info:
            if request.form['password'] == user_info[request.form['id']]:
                return redirect(url_for('index'))
        error = '아이디 또는 비밀번호가 틀렸습니다.'
        return render_template('login.html', error=error)
    else:
        return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'GET':
        return render_template('register.html', error=error)
    else:
        print(request.form['id'], request.form['password'])
        if request.form['id'] in user_info:
            error = '이미 아이디가 존재합니다.'
            return render_template('register.html', error=error)
        else:
            user_info[request.form['id']] = request.form['password']
            session['id'] = request.form['id']
            session['password'] = request.form['password']
            return redirect(url_for('login'))


@app.route('/user')
def profile():
    if session.get('id') is None:
        return redirect('/login')
    else:
        return render_template('userInfo', name=session.get('id'), password=session.get('password'))


with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

if __name__ == "__main__":
    app.run()
