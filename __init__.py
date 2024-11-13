from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)

    # db.create_all()로 데이터베이스 초기화
    with app.app_context():
        db.create_all()

    from .views.views import app as app_blueprint
    app.register_blueprint(app_blueprint)

    return app
