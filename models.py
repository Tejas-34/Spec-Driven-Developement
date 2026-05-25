from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    streak = db.Column(db.Integer, default=0)
    last_activity_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to FocusSession
    sessions = db.relationship('FocusSession', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class FocusSession(db.Model):
    __tablename__ = 'focus_session'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False) # e.g., Study, Coding, Revision, Design
    duration = db.Column(db.Integer, nullable=False)    # duration in minutes
    distractions = db.Column(db.Integer, default=0)
    score = db.Column(db.Integer, nullable=True)         # FocusMinutes - 2 * Distractions
    notes_learned = db.Column(db.Text, nullable=True)
    notes_mistakes = db.Column(db.Text, nullable=True)
    notes_revision = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='active', nullable=False) # active, completed, abandoned
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<FocusSession {self.title} - {self.status}>'
