from .. import db

class Mission(db.Model):
    __tablename__ = 'mission'

    missionId = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    diaryId = db.Column(db.Integer, db.ForeignKey('diary.diaryid'), nullable=False)

    diary = db.relationship('Diary', backref=db.backref('missions', lazy=True))