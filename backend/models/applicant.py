from datetime import datetime
from . import db

class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=True)
    email = db.Column(db.String(100), unique=False, nullable=True)
    phone_number = db.Column(db.String(15), unique=False, nullable=True)
    category = db.Column(db.String(100), unique=False, nullable=False)
    ai_score = db.Column(db.Float, nullable=False)
    resume_link = db.Column(db.String(5000), unique=False, nullable=False)
    summary = db.Column(db.String(10000), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    job_posting_id = db.Column(db.Integer, db.ForeignKey('job_posting.id'), nullable=False)    
