import os
import uuid
from flask import Blueprint, request, jsonify, send_from_directory, url_for
from models import db
from models.applicant import Applicant
from models.job_posting import JobPosting
from ai.extract_data import extract_data

job_posting_bp = Blueprint('job_posting_bp', __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESUMES_DIRECTORY = os.path.join(BASE_DIR, "resumes")

if not os.path.exists(RESUMES_DIRECTORY):
    os.makedirs(RESUMES_DIRECTORY)

@job_posting_bp.route('/', methods=['GET'])
def get_job_postings():
    job_postings = JobPosting.query.order_by(JobPosting.date_created.desc()).all()

    return jsonify(
        [
            {
                'id': job_posting.id,
                'title': job_posting.title,
                'description': job_posting.description,
                'resume_count': len(job_posting.applicants)
            }
            for job_posting in job_postings
        ])

@job_posting_bp.route('/', methods=['POST'])
def add_job_posting():
    data = request.get_json()
    new_job_posting = JobPosting(title=data['title'], description=data['description'])

    db.session.add(new_job_posting)
    db.session.commit()

    return jsonify(
        {
            'id': new_job_posting.id,
            'title': new_job_posting.title,
            'description': new_job_posting.description,
                'resume_count': len(new_job_posting.applicants)
        }), 201

@job_posting_bp.route('/<int:job_posting_id>', methods=['GET'])
def get_job_posting_with_applicants(job_posting_id):
    job_posting = JobPosting.query.get_or_404(job_posting_id)
    
    sorted_applicants = sorted(
        job_posting.applicants,
        key=lambda x: x.ai_score,
        reverse=True
    )

    applicants_list = [
        {
            'id': applicant.id,
            'name': applicant.name,
            'email': applicant.email,
            'phone_number': applicant.phone_number,
            'category': applicant.category,
            'ai_score': round(applicant.ai_score, 3),
            'resume_link': applicant.resume_link,
            'summary': applicant.summary,
        }
        for applicant in sorted_applicants
    ]

    return jsonify(
        {
            'id': job_posting.id,
            'title': job_posting.title,
            'description': job_posting.description,
            'applicants': applicants_list
        }
    )

@job_posting_bp.route('/<int:job_posting_id>', methods=['POST'])
def add_applicant(job_posting_id):
    if 'resume' not in request.files:
        return jsonify({'error': 'resume file is required'}), 400
    resume = request.files['resume']

    job_posting = JobPosting.query.get_or_404(job_posting_id)

    resume_filename = f"{uuid.uuid4()}.pdf"
    resume_path = os.path.join(RESUMES_DIRECTORY, resume_filename)
    resume.save(resume_path)

    resume_link = url_for('job_posting_bp.download_resume', filename=resume_filename, _external=True)

    ai_score, summary, category, full_name, phone_number, email = extract_data(resume, job_posting.description)

    new_applicant = Applicant(
        name=full_name,
        email=email,
        phone_number=phone_number,
        category=category,
        ai_score=ai_score,
        resume_link=resume_link,
        summary=summary,
        job_posting_id=job_posting_id
    )

    db.session.add(new_applicant)
    db.session.commit()

    print(new_applicant)

    return jsonify(
        {
            'id': new_applicant.id,
            'name': new_applicant.name,
            'email': new_applicant.email,
            'phone_number': new_applicant.phone_number,
            'category': new_applicant.category,
            'ai_score': new_applicant.ai_score,
            'resume_link': new_applicant.resume_link,
            'summary': new_applicant.summary,
            'job_posting_id': new_applicant.job_posting_id
        }
    ), 201

@job_posting_bp.route('/Download/<filename>', methods=['GET'])
def download_resume(filename):
    return send_from_directory(RESUMES_DIRECTORY, filename, as_attachment=True)
