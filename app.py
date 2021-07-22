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

board = [

]


# 메인페이지
@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', bd=board)


# 로그인
# GET -> 로그인 페이지
# POST -> 아이디 조회 후 로그인
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['id'] in user_info:
            if request.form['password'] == user_info[request.form['id']]:
                return redirect(url_for('index'))
        error = '아이디 또는 비밀번호가 틀렸습니다.'
        return render_template('login.html', error=error)
    else:
        return render_template('login.html', error=error)


# 회원가입
# GET -> 회원가입 페이지
# POST -> 이미 가입됐으면 error, 없으면 가입
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


# 유저 정보
# 로그인 하지 않은 상태면 로그인 페이지, 했다면 정보 출력
@app.route('/user')
def profile():
    if session.get('id') is None:
        return redirect('/login')
    else:
        return render_template('userInfo.html', name=session.get('id'), password=session.get('password'))


# 게시판 작성
@app.route('/write', methods=['GET', 'POST'])
def write():
    error = None
    if request.method == 'GET':
        if session.get('id') is None:
            error = '로그인 후 이용해주세요.'
            return redirect(url_for('login'))
        else:
            return render_template('write.html', error=error)
    else:
        if (request.form['title'] == '') | (request.form['content'] == ''):
            error = '제목 또는 내용을 입력해 주십시오.'
            return render_template('write.html', error=error)
        else:
            seq = len(board)
            board.append({'id': seq, 'title': request.form['title'], 'content': request.form['content'],
                          'writer': session.get('id')})
            return redirect(url_for('index'))


# 게시판
@app.route('/board/<int:bd_id>')
def boards(bd_id):
    return render_template('board.html', bd=board[bd_id])


if __name__ == "__main__":
    app.run()
