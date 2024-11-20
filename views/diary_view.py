from datetime import datetime
from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from semi.controllers.diary_controllers import get_analyses_by_diary, get_diary_by_date, get_disease_name, save_diary
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
            return redirect(url_for('diary_bp.view_diary', date=datetime.date.today().strftime('%Y-%m-%d')))

        flash('일기가 저장되었습니다.')
        return redirect(url_for('diary_bp.view_diary', date=datetime.date.today().strftime('%Y-%m-%d')))
    
    current_date = datetime.now().strftime("%Y년 %m월 %d일")
    return render_template('diaryWrite.html', current_date=current_date)

@diary_bp.route('/diary', methods=['GET'])
@login_required
def view_diary():
    uid = session.get('uid')
    date_str = request.args.get('date')
    if date_str:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        selected_date = datetime.date.today()
    
    diary = get_diary_by_date(uid, selected_date)
    if not diary:
        flash(f"{selected_date.strftime('%Y-%m-%d')}에 작성된 일기가 없습니다.")
        return render_template('diaryDetail.html', diary=None)
    
    analyses = get_analyses_by_diary(diary.diaryid)
    # 가장 높은 확률의 질병 찾기
    highest_analysis = max(analyses, key=lambda a: a.probability)
    highest_disease_name = get_disease_name(highest_analysis.diseaseId)
    highest_probability = highest_analysis.probability

    return render_template(
        'diaryDetail.html',
        diary=diary,
        analyses=analyses,
        highest_disease_name=highest_disease_name,
        highest_probability=highest_probability
    )