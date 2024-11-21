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

# 우울증 자가진단 결과 처리
@app.route('/submit_depression', methods=['POST'])
def submit_depression():
    total_score = 0
    for i in range(1, 21):  # 질문 1부터 20까지
        question_value = request.form.get(f'question{i}')
        if question_value:
            total_score += int(question_value)

    # 점수 25점 이상이면 응급콜 페이지로 리디렉션
    if total_score >= 25:
        return redirect(url_for('app_bp.emergency_call'))  # 응급콜 페이지로 리디렉션
    else:
        result = f"우울증 가능성 점수: {total_score}. 추가적인 조치를 취하는 것이 좋습니다."
        return render_template('result.html', result=result)

# 정신건강 위기상담 페이지 (emergency_call.html)
@app.route('/emergency_call')
def emergency_call():
    return render_template('emergency_call.html')