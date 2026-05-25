from datetime import date, datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, default="")
    theme = db.Column(db.String(20), default="dark", nullable=False)
    daily_target_minutes = db.Column(db.Integer, default=120, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    sessions = db.relationship("FocusSession", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def total_focus_minutes_today(self):
        today = date.today()
        return sum(
            session.duration_minutes
            for session in self.sessions
            if session.completed and session.started_at and session.started_at.date() == today
        )

    def current_streak(self):
        completed_dates = sorted(
            {
                session.started_at.date()
                for session in self.sessions
                if session.completed and session.started_at is not None
            },
            reverse=True,
        )
        if not completed_dates:
            return 0

        streak = 0
        cursor = date.today()
        if completed_dates[0] != cursor:
            if completed_dates[0] != cursor.fromordinal(cursor.toordinal() - 1):
                return 0
            cursor = completed_dates[0]

        date_set = set(completed_dates)
        while cursor in date_set:
            streak += 1
            cursor = cursor.fromordinal(cursor.toordinal() - 1)
        return streak

    def completed_sessions_count(self):
        return sum(1 for session in self.sessions if session.completed)

    def productivity_average(self):
        completed = [session.productivity_score for session in self.sessions if session.completed]
        return round(sum(completed) / len(completed), 1) if completed else 0


class FocusSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(140), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    goal = db.Column(db.Text, default="")
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ended_at = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    distraction_count = db.Column(db.Integer, default=0, nullable=False)
    learned_notes = db.Column(db.Text, default="")
    mistakes_notes = db.Column(db.Text, default="")
    revision_points = db.Column(db.Text, default="")
    reflection = db.Column(db.Text, default="")
    productivity_score = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def calculate_productivity_score(self):
        return max(self.duration_minutes - (2 * self.distraction_count), 0)

    def mark_completed(self):
        self.completed = True
        self.ended_at = self.ended_at or datetime.utcnow()
        self.productivity_score = self.calculate_productivity_score()
