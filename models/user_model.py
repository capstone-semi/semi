from .. import db

class User(db.Model):
    __tablename__ = 'user'
    
    uid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.Boolean)
    diagnosis = db.Column(db.String(100), nullable=True)

    diaries = db.relationship('Diary', backref='author', lazy=True)
