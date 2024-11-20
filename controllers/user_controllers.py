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

def load_user_data(uid):
    # User 모델을 사용하여 uid에 해당하는 사용자 정보 조회
    user = User.query.filter_by(uid=uid).first()
    if user:
        return {
            'nickname': user.nickname,
            'age': user.age,
            'gender': user.gender,
            'diagnosis': user.diagnosis
        }
    else:
        return None  # 사용자 정보가 없는 경우 None 반환
    