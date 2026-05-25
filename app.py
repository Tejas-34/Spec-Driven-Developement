import os
from flask import Flask
from extensions import db, login_manager
from models import User

def create_app():
    app = Flask(__name__)
    
    # Configure Application secret keys and SQLite Database file
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'premium-focus-sprint-secret-key-18239')
    
    # Place database.db in the root project folder
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize Shared Extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # User Loader for Flask-Login sessions
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    # Register Modular Blueprints
    from routes.auth import auth as auth_blueprint
    from routes.dashboard import dashboard as dashboard_blueprint
    from routes.session import session_bp as session_blueprint
    from routes.history import history as history_blueprint
    from routes.analytics import analytics as analytics_blueprint
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(session_blueprint)
    app.register_blueprint(history_blueprint)
    app.register_blueprint(analytics_blueprint)
    
    # Auto-create all relational database tables
    with app.app_context():
        db.create_all()
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
