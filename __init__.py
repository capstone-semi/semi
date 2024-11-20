from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from .config import Config
import os
from dotenv import load_dotenv

db = SQLAlchemy()

# .env 파일 로드
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    secret_key = os.getenv('SECRET_KEY', os.urandom(24))
    app.secret_key = secret_key
    
    db.init_app(app)

    # db.create_all()로 데이터베이스 초기화
    with app.app_context():
        from .models import user_model, diary_model
        db.create_all()

    # 블루프린트 등록
    from .views.views import app as app_bp
    app.register_blueprint(app_bp)
    
    from .views.user_view import user_bp
    app.register_blueprint(user_bp)

    from .views.diary_view import diary_bp
    app.register_blueprint(diary_bp, url_prefix='/diary')

    return app
