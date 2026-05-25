import os
from datetime import date, datetime, timedelta
from random import randint

from flask import Flask

from extensions import db, login_manager
from models import FocusSession, User


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "focussprint-dev-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///database.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.session import session_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(session_bp)

    @app.context_processor
    def inject_globals():
        return {"current_year": datetime.utcnow().year}

    @app.shell_context_processor
    def shell_context():
        return {"db": db, "User": User, "FocusSession": FocusSession}

    with app.app_context():
        db.create_all()

    @app.cli.command("seed")
    def seed_command():
        seed_database()
        print("Sample data created.")

    return app


def seed_database():
    if User.query.filter_by(email="demo@focussprint.app").first():
        return

    demo_user = User(
        username="DemoUser",
        email="demo@focussprint.app",
        bio="CS student preparing for placements and DSA interviews.",
        daily_target_minutes=180,
    )
    demo_user.set_password("demo1234")
    db.session.add(demo_user)
    db.session.flush()

    base_titles = [
        ("Graphs revision", "DSA"),
        ("System design notes", "Interview"),
        ("Operating systems", "College"),
        ("Mock coding round", "Practice"),
        ("Resume bullet cleanup", "Career"),
    ]

    for day_offset in range(8):
        session_date = date.today() - timedelta(days=day_offset)
        sessions_for_day = 1 if day_offset not in (3, 6) else 2
        for item in range(sessions_for_day):
            title, category = base_titles[(day_offset + item) % len(base_titles)]
            duration = [25, 45, 60][(day_offset + item) % 3]
            distractions = randint(0, 3)
            started_at = datetime.combine(session_date, datetime.min.time()) + timedelta(
                hours=7 + item * 2
            )
            ended_at = started_at + timedelta(minutes=duration)
            session = FocusSession(
                user_id=demo_user.id,
                title=title,
                category=category,
                duration_minutes=duration,
                goal="Stay focused and finish the planned milestone.",
                started_at=started_at,
                ended_at=ended_at,
                completed=True,
                distraction_count=distractions,
                learned_notes="Captured key takeaways from the sprint.",
                mistakes_notes="Need to reduce context switching.",
                revision_points="Revise again during weekend.",
                reflection="Strong momentum once the first 10 minutes passed.",
            )
            session.productivity_score = session.calculate_productivity_score()
            db.session.add(session)

    db.session.commit()


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
