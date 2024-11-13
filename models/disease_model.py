from .. import db

class Disease(db.Model):
    __tablename__ = 'disease'
    
    diseaseId = db.Column(db.Integer, primary_key=True)
    diseasename = db.Column(db.String(100), nullable=False)
