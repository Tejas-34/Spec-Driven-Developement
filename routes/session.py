from datetime import datetime, timedelta

from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from extensions import db
from models import FocusSession

session_bp = Blueprint("session", __name__, url_prefix="/session")


def get_owned_session(session_id):
    session = FocusSession.query.get_or_404(session_id)
    if session.user_id != current_user.id:
        abort(403)
    return session


@session_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_session():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip() or "General"
        selected_duration = request.form.get("duration_minutes", "25")
        custom_duration = request.form.get("custom_duration", "").strip()
        goal = request.form.get("goal", "").strip()
        duration = 25

        if selected_duration == "custom" and custom_duration.isdigit():
            duration = max(int(custom_duration), 5)
        elif selected_duration.isdigit():
            duration = max(int(selected_duration), 5)

        if not title:
            flash("Task title is required.", "danger")
            return render_template("session_create.html")

        focus_session = FocusSession(
            user_id=current_user.id,
            title=title,
            category=category,
            duration_minutes=duration,
            goal=goal,
            started_at=datetime.utcnow(),
            ended_at=datetime.utcnow() + timedelta(minutes=duration),
            productivity_score=duration,
        )
        db.session.add(focus_session)
        db.session.commit()
        flash("Focus session created.", "success")
        return redirect(url_for("session.active_session", session_id=focus_session.id))

    return render_template("session_create.html")


@session_bp.route("/<int:session_id>")
@login_required
def active_session(session_id):
    focus_session = get_owned_session(session_id)
    return render_template("session.html", focus_session=focus_session)


@session_bp.route("/<int:session_id>/distract", methods=["POST"])
@login_required
def distract(session_id):
    focus_session = get_owned_session(session_id)
    focus_session.distraction_count += 1
    focus_session.productivity_score = focus_session.calculate_productivity_score()
    db.session.commit()
    return jsonify(
        {
            "distractions": focus_session.distraction_count,
            "productivity_score": focus_session.productivity_score,
        }
    )


@session_bp.route("/<int:session_id>/complete", methods=["POST"])
@login_required
def complete_session(session_id):
    focus_session = get_owned_session(session_id)
    data = request.get_json(silent=True) or {}
    focus_session.learned_notes = data.get("learned_notes", "").strip()
    focus_session.mistakes_notes = data.get("mistakes_notes", "").strip()
    focus_session.revision_points = data.get("revision_points", "").strip()
    focus_session.reflection = data.get("reflection", "").strip()
    focus_session.ended_at = datetime.utcnow()
    focus_session.mark_completed()
    db.session.commit()
    return jsonify({"redirect_url": url_for("main.history")})


@session_bp.route("/<int:session_id>/reset", methods=["POST"])
@login_required
def reset_session(session_id):
    focus_session = get_owned_session(session_id)
    focus_session.distraction_count = 0
    focus_session.started_at = datetime.utcnow()
    focus_session.ended_at = focus_session.started_at + timedelta(minutes=focus_session.duration_minutes)
    focus_session.productivity_score = focus_session.duration_minutes
    db.session.commit()
    return jsonify({"status": "ok"})
