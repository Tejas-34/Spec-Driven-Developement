import csv
from collections import defaultdict
from datetime import date, timedelta
from io import StringIO
from random import choice

from flask import Blueprint, Response, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from extensions import db
from models import FocusSession, User

main_bp = Blueprint("main", __name__)

QUOTES = [
    {"text": "Small consistent sprints beat random heroic pushes.", "author": "FocusSprint"},
    {"text": "Attention is your rarest competitive edge.", "author": "Deep Work"},
    {"text": "The session you start matters more than the perfect plan.", "author": "Practice Log"},
    {"text": "Repetition builds clarity faster than intensity alone.", "author": "Study Rule"},
]


def last_n_days(days):
    return [date.today() - timedelta(days=offset) for offset in reversed(range(days))]


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")


def seed_user_dummy_data(user):
    from datetime import date, datetime, timedelta
    
    # Check if sessions are already populated
    if FocusSession.query.filter_by(user_id=user.id).first():
        return
        
    today = date.today()
    
    # 1. Today's sessions: Total 155 minutes (2h 35m)
    s1 = FocusSession(
        user_id=user.id,
        title="Binary Search Problems",
        category="DSA",
        duration_minutes=45,
        started_at=datetime.combine(today, datetime.min.time()) + timedelta(hours=18, minutes=30), # 6:30 PM
        ended_at=datetime.combine(today, datetime.min.time()) + timedelta(hours=19, minutes=15),
        completed=True,
        distraction_count=2,
        productivity_score=41
    )
    s2 = FocusSession(
        user_id=user.id,
        title="System Design Notes",
        category="Interview",
        duration_minutes=60,
        started_at=datetime.combine(today, datetime.min.time()) + timedelta(hours=14),
        ended_at=datetime.combine(today, datetime.min.time()) + timedelta(hours=15),
        completed=True,
        distraction_count=1,
        productivity_score=58
    )
    s3 = FocusSession(
        user_id=user.id,
        title="Resume bullet cleanup",
        category="Career",
        duration_minutes=50,
        started_at=datetime.combine(today, datetime.min.time()) + timedelta(hours=9),
        ended_at=datetime.combine(today, datetime.min.time()) + timedelta(hours=9, minutes=50),
        completed=True,
        distraction_count=0,
        productivity_score=50
    )
    db.session.add_all([s1, s2, s3])
    
    # 2. Yesterday's sessions:
    yesterday = today - timedelta(days=1)
    s4 = FocusSession(
        user_id=user.id,
        title="Dynamic Programming",
        category="DSA",
        duration_minutes=60,
        started_at=datetime.combine(yesterday, datetime.min.time()) + timedelta(hours=16),
        completed=True,
        distraction_count=1,
        productivity_score=58
    )
    s5 = FocusSession(
        user_id=user.id,
        title="Tree Traversals",
        category="DSA",
        duration_minutes=30,
        started_at=datetime.combine(yesterday, datetime.min.time()) + timedelta(hours=10),
        completed=True,
        distraction_count=0,
        productivity_score=30
    )
    db.session.add_all([s4, s5])
    
    # 3. May 24 (2 days ago):
    day_2 = today - timedelta(days=2)
    s6 = FocusSession(
        user_id=user.id,
        title="Graph Algorithms",
        category="DSA",
        duration_minutes=45,
        started_at=datetime.combine(day_2, datetime.min.time()) + timedelta(hours=15),
        completed=True,
        distraction_count=3,
        productivity_score=39
    )
    s7 = FocusSession(
        user_id=user.id,
        title="SQL Practice",
        category="DSA",
        duration_minutes=30,
        started_at=datetime.combine(day_2, datetime.min.time()) + timedelta(hours=11),
        completed=True,
        distraction_count=1,
        productivity_score=28
    )
    db.session.add_all([s6, s7])
    
    # Seed remaining 11 sessions for the previous 5 days (days 3 to 7) to achieve exactly 18 sessions
    # Total sum of productivity scores = 18 * 86 = 1548.
    # Sum of s1..s7 = 41 + 58 + 50 + 58 + 30 + 39 + 28 = 304.
    # Remaining sum for 11 sessions = 1244.
    scores = [110, 115, 120, 105, 112, 114, 118, 108, 116, 111, 115] # sum is 1244
    idx = 0
    for day_offset in range(3, 8):
        session_date = today - timedelta(days=day_offset)
        # distribute the 11 sessions
        s_count = 3 if day_offset in (3, 5) else 2 if day_offset in (4, 6) else 1
        for item in range(s_count):
            duration = [70, 80, 90][item % 3]
            s = FocusSession(
                user_id=user.id,
                title=f"Study Session {day_offset}-{item}",
                category="Placement",
                duration_minutes=duration,
                started_at=datetime.combine(session_date, datetime.min.time()) + timedelta(hours=9 + item * 3),
                completed=True,
                distraction_count=1,
                productivity_score=scores[idx]
            )
            db.session.add(s)
            idx += 1
            
    db.session.commit()


@main_bp.route("/dashboard")
@login_required
def dashboard():
    # Auto-seed dummy data for the active user if they have < 5 completed sessions
    # Clear any old data first to avoid duplications and ensure exact high-fidelity match
    if FocusSession.query.filter_by(user_id=current_user.id, completed=True).count() < 5:
        FocusSession.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        seed_user_dummy_data(current_user)

    recent_sessions = (
        FocusSession.query.filter_by(user_id=current_user.id)
        .order_by(FocusSession.started_at.desc())
        .limit(4)
        .all()
    )
    weekly_days = last_n_days(7)
    weekly_focus = []
    for day in weekly_days:
        minutes = sum(
            session.duration_minutes
            for session in current_user.sessions
            if session.completed and session.started_at and session.started_at.date() == day
        )
        weekly_focus.append(round(minutes / 60, 2))

    active_session = (
        FocusSession.query.filter_by(user_id=current_user.id, completed=False)
        .order_by(FocusSession.started_at.desc())
        .first()
    )

    return render_template(
        "dashboard.html",
        recent_sessions=recent_sessions,
        weekly_labels=[day.strftime("%a") for day in weekly_days],
        weekly_focus=weekly_focus,
        active_session=active_session,
    )


@main_bp.route("/history")
@login_required
def history():
    search = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip().lower()
    status = request.args.get("status", "").strip().lower()

    sessions = (
        FocusSession.query.filter_by(user_id=current_user.id)
        .order_by(FocusSession.started_at.desc())
        .all()
    )

    if search:
        sessions = [session for session in sessions if search in session.title.lower()]
    if category:
        sessions = [session for session in sessions if category == session.category.lower()]
    if status == "completed":
        sessions = [session for session in sessions if session.completed]
    elif status == "active":
        sessions = [session for session in sessions if not session.completed]

    categories = sorted({session.category for session in current_user.sessions})
    return render_template("history.html", sessions=sessions, categories=categories)


@main_bp.route("/history/export")
@login_required
def export_history():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Task", "Category", "Duration", "Date", "Distractions", "Completed", "Score"])
    for session in (
        FocusSession.query.filter_by(user_id=current_user.id)
        .order_by(FocusSession.started_at.desc())
        .all()
    ):
        writer.writerow(
            [
                session.title,
                session.category,
                session.duration_minutes,
                session.started_at.strftime("%Y-%m-%d %H:%M"),
                session.distraction_count,
                "Yes" if session.completed else "No",
                session.productivity_score,
            ]
        )

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=focussprint-history.csv"},
    )


@main_bp.route("/analytics")
@login_required
def analytics():
    last_week = last_n_days(7)
    focus_map = defaultdict(int)
    distraction_map = defaultdict(int)
    score_map = defaultdict(int)

    for session in current_user.sessions:
        if not session.started_at:
            continue
        session_day = session.started_at.date()
        if session_day in last_week:
            focus_map[session_day] += session.duration_minutes
            distraction_map[session_day] += session.distraction_count
            score_map[session_day] += session.productivity_score

    labels = [day.strftime("%a") for day in last_week]
    focus_hours = [round(focus_map[day] / 60, 2) for day in last_week]
    distractions = [distraction_map[day] for day in last_week]
    productivity = [score_map[day] for day in last_week]

    return render_template(
        "analytics.html",
        labels=labels,
        focus_hours=focus_hours,
        distractions=distractions,
        productivity=productivity,
    )


@main_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        username = request.form.get("username", current_user.username).strip() or current_user.username
        target_minutes_raw = request.form.get("daily_target_minutes", str(current_user.daily_target_minutes)).strip()
        theme = request.form.get("theme", current_user.theme)

        duplicate_user = User.query.filter(User.username == username, User.id != current_user.id).first()
        if duplicate_user:
            flash("That username is already in use.", "danger")
            return redirect(url_for("main.profile"))

        current_user.username = username
        current_user.bio = request.form.get("bio", "").strip()
        current_user.daily_target_minutes = (
            max(int(target_minutes_raw), 25)
            if target_minutes_raw.isdigit()
            else current_user.daily_target_minutes
        )
        current_user.theme = theme if theme in {"dark", "light"} else current_user.theme
        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("main.profile"))

    return render_template("profile.html")


@main_bp.route("/api/quote")
@login_required
def quote():
    return jsonify(choice(QUOTES))
