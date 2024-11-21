import datetime
from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify, session

from semi.controllers.diary_controllers import get_analyses_by_diary, get_diary_by_date, get_disease_name
from semi.controllers.user_controllers import load_user_data
from .. import db
from semi.models.user_model import User

# user 블루프린트 생성
user_bp = Blueprint('user_bp', __name__)

def is_logged_in():
    return 'uid' in session\
    
def login_required(func):
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('user_bp.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

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
        data = request.get_json()
        user_id = data.get('id')
        password = data.get('password')

        user = User.query.filter_by(id=user_id).first()
        if user and user.check_password(password):  # 비밀번호 확인
            # 로그인 성공, 세션에 사용자 정보 저장
            session['uid'] = user.uid  # 사용자 고유 ID
            session['username'] = user.nickname  # 사용자 닉네임
            return jsonify({'success': True, 'message': '로그인 성공'}), 200  # JSON 응답
        else:
            # 로그인 실패, JSON 에러 메시지 반환
            return jsonify({'success': False, 'message': "아이디나 비밀번호가 일치하지 않습니다."}), 401

    return render_template('index.html')

@user_bp.route('/home', methods=['GET'])
@login_required
def home():
    uid = session.get('uid')
    user_data = load_user_data(uid)

    # 날짜 선택 기능
    date_str = request.args.get('date')
    try:
        if date_str:
            selected_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            selected_date = datetime.date.today()
    except ValueError:
        # 날짜 형식이 잘못된 경우 기본값으로 오늘 날짜 설정
        selected_date = datetime.date.today()

    # 변수를 미리 초기화
    highest_disease_name = None
    highest_probability = None
        
    diary = get_diary_by_date(uid, selected_date)
    if diary:
        analyses = get_analyses_by_diary(diary.diaryid)
        if analyses:  # analyses가 비어 있지 않은 경우
            highest_analysis = max(analyses, key=lambda a: a.probability)
            highest_disease = highest_analysis.disease
            highest_probability = highest_analysis.probability
        else:
            highest_disease = None
            highest_probability = None
    else:
        analyses = []
        highest_disease_name = None
        highest_probability = None

    return render_template(
        'home.html',
        user_data=user_data,
        diary=diary,
        analyses=analyses,
        highest_disease_name=highest_disease_name,
        highest_probability=highest_probability,
        selected_date=selected_date
    )

@user_bp.route('/logout')
def logout():
    session.pop('uid', None) 
    session.pop('username', None)  
    flash("로그아웃 되었습니다.")
    return redirect(url_for('user_bp.login'))

@user_bp.route('/mypage')
@login_required  
def mypage():
    uid = session.get('uid')  # 세션에서 uid 가져오기
    if not uid:
        flash("로그인이 필요합니다.")
        return redirect(url_for('user_bp.login'))
    user_data = load_user_data(uid)
    if not user_data:
        flash("사용자 정보를 찾을 수 없습니다.")
        return redirect(url_for('user_bp.login'))

    return render_template('mypage.html', user_data=user_data)
