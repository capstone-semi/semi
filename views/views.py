from urllib import request
from flask import Blueprint,render_template, request, url_for, redirect

from semi.views.user_view import login_required

app = Blueprint('app_bp', __name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

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

@app.route('/depression')
def depression():
    return render_template('depression.html')

@app.route('/bipolar')
def bipolar():
    return render_template('bipolar.html')

@app.route('/ptsd')
def ptsd():
    return render_template('ptsd.html')

@app.route('/adhd')
def adhd():
    return render_template('adhd.html')

@app.route('/anxiety')
def anxiety():
    return render_template('anxiety.html')

# 정신건강 위기상담 페이지 (emergency_call.html)
@app.route('/emergency_call')
def emergency_call():
    return render_template('emergency_call.html')

@app.route('/hospital')
def hospital():
    return render_template('hospital.html')