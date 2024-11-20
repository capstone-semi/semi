from flask import Blueprint, render_template

from semi.views.user_view import login_required

app = Blueprint('app_bp', __name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/diaryWrite')
@login_required
def diaryWrite():
    return render_template('diaryWrite.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/challenge')
@login_required
def challenge():
    return render_template('challenge.html')

@app.route('/result')
@login_required
def result():
    return render_template('result.html')

@app.route('/call')
def call():
    return render_template('call.html')
