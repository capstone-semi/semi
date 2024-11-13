from .. import db

class Diary(db.Model):
    __tablename__ = 'diary'
    
    diaryid = db.Column(db.Integer, primary_key=True)
    diarydate = db.Column(db.Date, default=db.func.current_timestamp())
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
