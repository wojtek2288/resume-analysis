from flask import Flask
from models import db
from routes.job_posting import job_posting_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    CORS(app, resources={r"/*": {"origins": "*"}})
    app.register_blueprint(job_posting_bp, url_prefix='/JobPostings')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
