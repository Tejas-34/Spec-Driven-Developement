import io
import csv
from datetime import datetime
from flask import Blueprint, render_template, make_response
from flask_login import login_required, current_user
from extensions import db
from models import FocusSession

history = Blueprint('history', __name__, url_prefix='/history')

@history.route('/')
@login_required
def view_history():
    # Query all focus sessions for this user, ordered by date desc
    sessions = FocusSession.query.filter_by(user_id=current_user.id).order_by(FocusSession.created_at.desc()).all()
    categories = db.session.query(FocusSession.category).filter_by(user_id=current_user.id).distinct().all()
    categories_list = [c[0] for c in categories if c[0]]
    
    return render_template('history.html', sessions=sessions, categories=categories_list)

@history.route('/export')
@login_required
def export_csv():
    sessions = FocusSession.query.filter_by(user_id=current_user.id).order_by(FocusSession.created_at.desc()).all()
    
    # Generate CSV stream in-memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow(['Session ID', 'Task Title', 'Category', 'Duration (Minutes)', 'Distractions', 'Productivity Score', 'Status', 'Date Completed', 'Things Learned', 'Mistakes Made', 'Next Revision Steps'])
    
    # Rows
    for s in sessions:
        created_str = s.created_at.strftime('%Y-%m-%d %H:%M:%S') if s.created_at else ''
        writer.writerow([
            s.id,
            s.title,
            s.category,
            s.duration,
            s.distractions,
            s.score if s.score is not None else '',
            s.status,
            created_str,
            s.notes_learned or '',
            s.notes_mistakes or '',
            s.notes_revision or ''
        ])
        
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename=focussprint_history_{datetime.now().strftime('%Y%md')}.csv"
    response.headers["Content-type"] = "text/csv"
    return response
