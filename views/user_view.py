from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify, session
from .. import db
from semi.models.user_model import User

# app 블루프린트 생성
app_bp = Blueprint('app_bp', __name__)
# user 블루프린트 생성
user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        id = request.form.get('id')
        password = request.form.get('password')
        nickname = request.form.get('nickname')
        age = request.form.get('age')
        gender = request.form.get('gender') == 'male'
        diagnosis = request.form.get('diagnosis')

        # 사용자 중복 체크
        user_exists = User.query.filter_by(id=id).first()
        if user_exists:
            return render_template(
                'signup.html',
                error_title="유효하지 않는 입력값",
                error_message="이미 존재하는 아이디입니다. 다른 아이디를 입력해주세요."
            )
        new_user = User(id=id, nickname=nickname, age=age, gender=gender, diagnosis=diagnosis)
        new_user.set_password(password)  # 비밀번호 해싱
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful.')
        return redirect(url_for('app_bp.main'))

    return render_template('signup.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # JSON 데이터 수신
        data = request.get_json()
        user_id = data.get('id')
        password = data.get('password')
        
        user = User.query.filter_by(id=user_id).first()
        if user and user.check_password(password):  # 비밀번호 해싱 시 check_password 사용
            # 로그인 성공
            session['user_id'] = user.uid
            session['username'] = user.nickname
            return jsonify({'success': True}), 200
        else:
            # 로그인 실패
            return jsonify({'success': False, 'message': "아이디가 일치하지 않습니다."}), 401
    
    return render_template('login.html')