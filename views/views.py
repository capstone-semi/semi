from flask import Blueprint, render_template
from semi.models.user_model import User

app = Blueprint('app', __name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/challenge')
def challenge():
    return render_template('challenge.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/call')
def call():
    return render_template('call.html')
