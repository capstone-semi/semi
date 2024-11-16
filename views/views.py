from flask import Blueprint, render_template

app = Blueprint('app_bp', __name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home')
def home():
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
