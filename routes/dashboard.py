import random
from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models import FocusSession, User

dashboard = Blueprint('dashboard', __name__)

MOTIVATIONAL_QUOTES = [
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"text": "Focus is a matter of deciding what things you're not going to do.", "author": "John Carmack"},
    {"text": "Amateurs sit and wait for inspiration, the rest of us just get up and go to work.", "author": "Stephen King"},
    {"text": "It is not that I am so smart, it's just that I stay with problems longer.", "author": "Albert Einstein"},
    {"text": "Deep work is not some nostalgic affectation... It is instead an indispensable skill.", "author": "Cal Newport"},
    {"text": "Focus is a muscle, and you build it through practice.", "author": "FocusSprint"},
    {"text": "You do not rise to the level of your goals. You fall to the level of your systems.", "author": "James Clear"},
    {"text": "Small daily improvements over time lead to stunning results.", "author": "Robin Sharma"},
    {"text": "Make it work, make it right, make it fast.", "author": "Kent Beck"},
    {"text": "The pain of discipline is nothing compared to the pain of regret.", "author": "Anonymous"}
]

@dashboard.route('/')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
    return render_template('index.html')

@dashboard.route('/dashboard')
@login_required
def home():
    today = date.today()
    start_of_today = datetime.combine(today, datetime.min.time())
    
    # Calculate Today's metrics
    today_sessions = FocusSession.query.filter(
        FocusSession.user_id == current_user.id,
        FocusSession.created_at >= start_of_today,
        FocusSession.status == 'completed'
    ).all()
    
    today_focus_time = sum(s.duration for s in today_sessions)
    today_completed_count = len(today_sessions)
    
    # Total stats
    total_sessions_query = FocusSession.query.filter_by(user_id=current_user.id, status='completed')
    total_completed = total_sessions_query.count()
    
    # Average Productivity Score
    scores = [s.score for s in total_sessions_query.all() if s.score is not None]
    avg_score = round(sum(scores) / len(scores)) if scores else 0
    
    # Recent sessions (last 5)
    recent_sessions = FocusSession.query.filter_by(user_id=current_user.id).order_by(FocusSession.created_at.desc()).limit(5).all()
    
    # Get a random quote
    quote = random.choice(MOTIVATIONAL_QUOTES)
    
    return render_template(
        'dashboard.html',
        today_focus_time=today_focus_time,
        total_completed=total_completed,
        avg_score=avg_score,
        recent_sessions=recent_sessions,
        quote=quote
    )

@dashboard.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip().lower()
        
        if not username or not email:
            flash('All fields are required.', 'danger')
            return render_template('profile_settings.html')
            
        # Check duplicate username
        dup_user = User.query.filter(User.username == username, User.id != current_user.id).first()
        if dup_user:
            flash('Username is already taken.', 'danger')
            return render_template('profile_settings.html')
            
        # Check duplicate email
        dup_email = User.query.filter(User.email == email, User.id != current_user.id).first()
        if dup_email:
            flash('Email is already registered.', 'danger')
            return render_template('profile_settings.html')
            
        try:
            current_user.username = username
            current_user.email = email
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('dashboard.settings'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            
    return render_template('profile_settings.html')
