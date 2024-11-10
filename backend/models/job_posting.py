from datetime import datetime
from . import db

class JobPosting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(10000), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    applicants = db.relationship('Applicant', backref='job_posting', lazy=True)
