from flask import render_template, request, redirect, url_for, flash
from .. import db
from semi.models.user_model import User

def register():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        nickname = request.form['nickname']
        age = int(request.form['age']) if request.form['age'] else None
        gender = True if request.form['gender'] == 'male' else False
        diagnosis = request.form['diagnosis']

        user_exists = User.query.filter_by(id=id).first() is not None
        if user_exists:
            flash('ID already exists')
            return redirect(url_for('register'))

        new_user = User(id=id, password=password, nickname=nickname, age=age, gender=gender, diagnosis=diagnosis)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful')
        return redirect(url_for('login'))

    return render_template('signup.html')