import datetime
from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from semi.controllers.diary_controllers import get_analyses_by_diary, get_diary_by_date, get_disease_name, save_diary
from semi.models.mission_model import Mission
from semi.views.user_view import login_required

diary_bp = Blueprint('diary_bp', __name__)

@diary_bp.route('/diaryWrite', methods=['GET', 'POST'])
@login_required
def write_diary():
    uid = session.get('uid')
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            flash('제목과 내용을 모두 입력해주세요.')
            return redirect(url_for('diary_bp.write_diary'))
        
        diary = save_diary(uid, title, content)
        if diary is None:
            flash('오늘은 이미 일기를 작성하셨습니다.')
            return redirect(url_for('diary_bp.view_diary', date=datetime.datetime.today().strftime('%Y-%m-%d')))

        flash('일기가 저장되었습니다.')
        return redirect(url_for('diary_bp.view_diary', date=datetime.datetime.today().strftime('%Y-%m-%d')))
    
    # 오늘 날짜 생성
    current_date = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    return render_template('diaryWrite.html', current_date=current_date)

@diary_bp.route('/diary', methods=['GET'])
@login_required
def view_diary():
    uid = session.get('uid')
    date_str = request.args.get('date')
    try:
        selected_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.today().date()
    except ValueError:
        flash("날짜 형식이 잘못되었습니다. YYYY-MM-DD 형식을 사용해주세요.")
        selected_date = datetime.today().date()

    today = datetime.datetime.now().date()
    week_start = today - datetime.timedelta(days=3)
    dates = [(week_start + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

    diary = get_diary_by_date(uid, selected_date)

    formatted_selected_date = selected_date.strftime('%Y-%m-%d')  # 날짜를 문자열로 포맷
    formatted_today = today.strftime('%Y-%m-%d')
    
    if not diary:
        flash(f"{selected_date.strftime('%Y-%m-%d')}에 작성된 일기가 없습니다.")
        return render_template(
            'home.html',
            diary=None,
            selected_date=formatted_selected_date,
            dates=dates,
            today=formatted_today,
            analyses=[],  # 빈 분석 리스트도 전달
            highest_disease_name=None,
            highest_probability=None,
            mission=None
        )
    
    analyses = get_analyses_by_diary(diary.diaryid)
    if analyses:
        highest_analysis = max(analyses, key=lambda a: a.probability)
        highest_disease_name = get_disease_name(highest_analysis.diseaseId)
        highest_probability = highest_analysis.probability
    else:
        highest_disease_name = None
        highest_probability = None

    mission = Mission.query.filter_by(diaryId=diary.diaryid).first()

    return render_template(
        'home.html',
        diary=diary,
        analyses=analyses,
        highest_disease_name=highest_disease_name,
        highest_probability=highest_probability,
        selected_date=formatted_selected_date,
        dates=dates,
        today=formatted_today,
        mission=mission
    )