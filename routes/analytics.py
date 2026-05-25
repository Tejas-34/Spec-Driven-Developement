from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import FocusSession

analytics = Blueprint('analytics', __name__, url_prefix='/analytics')

@analytics.route('/')
@login_required
def view_analytics():
    return render_template('analytics.html')

@analytics.route('/data')
@login_required
def get_analytics_data():
    today = date.today()
    
    # We will compute data for the last 7 days (including today)
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    
    weekly_labels = []
    weekly_hours = []
    distraction_counts = []
    productivity_scores = []
    
    for d in days:
        day_name = d.strftime('%a') # Mon, Tue, etc.
        start_of_day = datetime.combine(d, datetime.min.time())
        end_of_day = datetime.combine(d, datetime.max.time())
        
        # Query completed sessions on this day
        sessions = FocusSession.query.filter(
            FocusSession.user_id == current_user.id,
            FocusSession.created_at >= start_of_day,
            FocusSession.created_at <= end_of_day,
            FocusSession.status == 'completed'
        ).all()
        
        # Focus hours
        total_mins = sum(s.duration for s in sessions)
        total_hours = round(total_mins / 60, 2)
        
        # Distractions
        total_distract = sum(s.distractions for s in sessions)
        
        # Productivity average
        scores = [s.score for s in sessions if s.score is not None]
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0
        
        weekly_labels.append(day_name)
        weekly_hours.append(total_hours)
        distraction_counts.append(total_distract)
        productivity_scores.append(avg_score)
        
    return jsonify({
        'weekly_labels': weekly_labels,
        'weekly_hours': weekly_hours,
        'distractions': distraction_counts,
        'productivity_scores': productivity_scores
    })
