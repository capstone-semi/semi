from .. import db

class Analysis(db.Model):
    __tablename__ = 'analysis'
    
    analysisId = db.Column(db.Integer, primary_key=True)
    diaryid = db.Column(db.Integer, db.ForeignKey('diary.diaryid'), nullable=False)
    diseaseId = db.Column(db.Integer, db.ForeignKey('disease.diseaseId'), nullable=False)
    probability = db.Column(db.Float, nullable=False)

    diary = db.relationship('Diary', back_populates='analyses')
    disease = db.relationship('Disease', back_populates='analyses')
