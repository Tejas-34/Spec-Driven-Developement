from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import FocusSession, User

session_bp = Blueprint('session', __name__, url_prefix='/session')

@session_bp.route('/new', methods=['GET', 'POST'])
@login_required
def start_session():
    # If there is already an active session, redirect to it!
    active_s = FocusSession.query.filter_by(user_id=current_user.id, status='active').first()
    if active_s:
        flash('You have an active session! Re-focusing.', 'info')
        return redirect(url_for('session.active_timer', session_id=active_s.id))
        
    if request.method == 'POST':
        title = request.form.get('title').strip()
        category = request.form.get('category')
        duration_option = request.form.get('duration')
        description = request.form.get('description', '').strip()
        
        if not title or not category or not duration_option:
            flash('All fields are required.', 'danger')
            return redirect(url_for('dashboard.home'))
            
        if duration_option == 'custom':
            try:
                duration = int(request.form.get('custom_minutes'))
                if duration <= 0 or duration > 180:
                    raise ValueError()
            except (TypeError, ValueError):
                flash('Please enter a valid custom duration between 1 and 180 minutes.', 'danger')
                return redirect(url_for('dashboard.home'))
        else:
            try:
                duration = int(duration_option)
            except ValueError:
                flash('Invalid duration selected.', 'danger')
                return redirect(url_for('dashboard.home'))
                
        # Create focus session
        new_session = FocusSession(
            user_id=current_user.id,
            title=title,
            category=category,
            duration=duration,
            notes_learned='',
            notes_mistakes='',
            notes_revision='',
            status='active'
        )
        
        try:
            db.session.add(new_session)
            db.session.commit()
            return redirect(url_for('session.active_timer', session_id=new_session.id))
        except Exception as e:
            db.session.rollback()
            flash('Failed to start session. Please try again.', 'danger')
            return redirect(url_for('dashboard.home'))
            
    return render_template('session_create.html')

@session_bp.route('/<int:session_id>')
@login_required
def active_timer(session_id):
    fs = FocusSession.query.get_or_4000 = FocusSession.query.get_or_404(session_id)
    if fs.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard.home'))
        
    if fs.status != 'active':
        flash('This session has already ended.', 'info')
        return redirect(url_for('dashboard.home'))
        
    return render_template('session.html', session=fs)

@session_bp.route('/<int:session_id>/distract', methods=['POST'])
@login_required
def log_distraction(session_id):
    fs = FocusSession.query.get_or_404(session_id)
    if fs.user_id != current_user.id or fs.status != 'active':
        return jsonify({'success': False, 'message': 'Invalid session'}), 400
        
    fs.distractions += 1
    try:
        db.session.commit()
        return jsonify({'success': True, 'distractions': fs.distractions})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Database error'}), 500

@session_bp.route('/<int:session_id>/abandon', methods=['POST'])
@login_required
def abandon_session(session_id):
    fs = FocusSession.query.get_or_404(session_id)
    if fs.user_id != current_user.id or fs.status != 'active':
        flash('Invalid session.', 'danger')
        return redirect(url_for('dashboard.home'))
        
    fs.status = 'abandoned'
    fs.score = 0
    try:
        db.session.commit()
        flash('Session abandoned.', 'warning')
    except Exception as e:
        db.session.rollback()
        
    return redirect(url_for('dashboard.home'))

@session_bp.route('/<int:session_id>/reflect', methods=['GET', 'POST'])
@login_required
def reflect(session_id):
    fs = FocusSession.query.get_or_404(session_id)
    if fs.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard.home'))
        
    if fs.status != 'active' and fs.status != 'completed':
        flash('This session is not in reflective state.', 'info')
        return redirect(url_for('dashboard.home'))
        
    if request.method == 'POST':
        learned = request.form.get('learned', '').strip()
        mistakes = request.form.get('mistakes', '').strip()
        revision = request.form.get('revision', '').strip()
        
        fs.notes_learned = learned
        fs.notes_mistakes = mistakes
        fs.notes_revision = revision
        fs.status = 'completed'
        
        # Calculate Productivity Score: FocusMinutes - 2 * Distractions
        fs.score = fs.duration - (2 * fs.distractions)
        
        # Streak System logic
        today_date = date.today()
        if current_user.last_activity_date is None:
            current_user.streak = 1
        else:
            diff = today_date - current_user.last_activity_date
            if diff.days == 1:
                # Consecutive day
                current_user.streak += 1
            elif diff.days > 1:
                # Missed a day, reset streak to 1
                current_user.streak = 1
            # If diff.days == 0 (completed another session today), streak remains unchanged
            
        current_user.last_activity_date = today_date
        
        try:
            db.session.commit()
            flash('Focus session logged and reflection recorded successfully!', 'success')
            return redirect(url_for('dashboard.home'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to save reflection notes. Please try again.', 'danger')
            
    return render_template('session_reflect.html', session=fs)
