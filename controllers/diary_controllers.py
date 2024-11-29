from datetime import date
import os
import random
import openai
from semi.models.analysis_model import Analysis
from semi.models.diary_model import Diary
from semi.models.mission_model import Mission
from semi import db
from semi.models.disease_model import Disease
from dotenv import load_dotenv
import openai

# .env 파일 로드
load_dotenv()

def save_diary(uid, title, content):
    # 오늘 날짜의 일기가 이미 있는지 확인
    existing_diary = Diary.query.filter_by(uid=uid, diarydate=date.today()).first()
    if existing_diary:
        return None  # 이미 일기가 있으면 None 반환

    new_diary = Diary(uid=uid, title=title, content=content)
    db.session.add(new_diary)
    db.session.commit()

    # 일기 저장 후 분석 수행
    perform_analysis(new_diary)

     # 미션 생성 및 저장
    generate_mission(new_diary)

    return new_diary

def perform_analysis(diary):
    # 질병 리스트 가져오기
    diseases = Disease.query.all()
    if not diseases:
        # 질병 데이터가 없으면 기본 질병 생성
        disease_names = ['ADHD', '우울증', '불안장애', 'PTSD', '조울증', '정상']
        for name in disease_names:
            disease = Disease(diseasename=name)
            db.session.add(disease)
        db.session.commit()
        diseases = Disease.query.all()

    # 임의의 확률 생성 (실제로는 NLP 모델 등을 사용)
    probabilities = {}
    for disease in diseases:
        probabilities[disease.diseaseId] = random.uniform(0, 100)

    # 확률의 합을 100으로 정규화
    total = sum(probabilities.values())
    for diseaseId in probabilities:
        probabilities[diseaseId] = (probabilities[diseaseId] / total) * 100

    # 가장 높은 확률의 질병 찾기
    highest_diseaseId = max(probabilities, key=probabilities.get)
    highest_probability = probabilities[highest_diseaseId]

    # 각 질병에 대한 분석 결과 저장
    for diseaseId, probability in probabilities.items():
        analysis = Analysis(
            diaryid=diary.diaryid,
            diseaseId=diseaseId,
            probability=probability
        )
        db.session.add(analysis)
    db.session.commit()

def get_diary_by_date(uid, selected_date):
    return Diary.query.filter_by(uid=uid, diarydate=selected_date).first()

def get_analyses_by_diary(diaryid):
    return Analysis.query.filter_by(diaryid=diaryid).all()

def get_disease_name(diseaseId):
    disease = Disease.query.get(diseaseId)
    return disease.diseasename if disease else 'Unknown'

def generate_mission(diary):
    # 분석 결과 가져오기
    analyses = get_analyses_by_diary(diary.diaryid)
    if not analyses:
        return

    # 가장 높은 확률의 질병 찾기
    highest_analysis = max(analyses, key=lambda a: a.probability)
    highest_disease_name = get_disease_name(highest_analysis.diseaseId)
    highest_probability = highest_analysis.probability

    # 보건복지부 추천 행동 가져오기
    recommended_actions = get_recommended_actions(highest_disease_name)

    # 프롬프트 생성
    if recommended_actions:
        prompt = f"""너는 심리상담가로써 다음 사람의 일기를 보고 100자 이내 적당한 미션 한 개를 줘야해.
                        제목: {diary.title}
                        내용: {diary.content}
                        정신질환 {highest_disease_name}일 확률 {highest_probability:.2f}%
                        보건복지부에서 해당 질환에 대해 추천하는 행동: {recommended_actions}
                    """
    else:
        prompt = f"""너는 심리상담가로써 다음 사람의 일기를 보고 100자 이내 적당한 미션 한 개를 줘야해.
                    제목: {diary.title}
                    내용: {diary.content}
                """

    # OpenAI API 키 설정 (환경 변수 또는 설정 파일에서 가져오기)
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # GPT-4 모델을 사용하여 미션 생성
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "당신은 전문 심리상담가입니다."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
    )

    mission_content = response.choices[0].message['content'].strip()

    # 미션을 데이터베이스에 저장
    new_mission = Mission(
        diaryId=diary.diaryid,
        content=mission_content
    )
    db.session.add(new_mission)
    db.session.commit()


def get_analyses_by_diary(diaryid):
    return Analysis.query.filter_by(diaryid=diaryid).all()

def get_disease_name(diseaseId):
    disease = Disease.query.get(diseaseId)
    return disease.diseasename if disease else 'Unknown'

def get_recommended_actions(disease_name):
    if disease_name == "정상":
        return None  # '정상'인 경우 추천 행동을 포함하지 않음
    try:
        # 현재 파일의 디렉토리를 기준으로 경로 설정
        base_dir = os.path.dirname(os.path.abspath(__file__))
        recommendations_path = os.path.join(base_dir, 'recommendations', f'{disease_name}.txt')
        with open(recommendations_path, 'r', encoding='utf-8') as file:
            recommendations = file.read()
        return recommendations
    except FileNotFoundError:
        return None  # 파일이 없으면 추천 행동을 포함하지 않음 ##