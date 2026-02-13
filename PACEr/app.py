import os
import secrets
from datetime import date, timedelta
from flask import Flask
from flask_login import LoginManager
from models import db, User
from werkzeug.security import generate_password_hash
from services.csrf import generate_csrf_token


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(16))

    # Session security
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Database config
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pacer.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'admin.admin_login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.home import bp_home
    from routes.calculator import bp_calculator
    from routes.report import bp_report
    from routes.admin import bp_admin
    from routes.tournament import bp_tournament

    app.register_blueprint(bp_home)
    app.register_blueprint(bp_calculator)
    app.register_blueprint(bp_report)
    app.register_blueprint(bp_admin)
    app.register_blueprint(bp_tournament)

    @app.context_processor
    def inject_globals():
        return {
            'current_year': date.today().year,
            'csrf_token': generate_csrf_token,
        }

    # Create tables and seed super admin
    with app.app_context():
        db.create_all()
        _seed_super_admin()

    return app


def _seed_super_admin():
    """Seed super admin user if not already present."""
    existing = User.query.filter_by(username='admin').first()
    if not existing:
        default_password = os.environ.get('ADMIN_PASSWORD', 'Potsdam1')
        user = User(
            username='admin',
            password_hash=generate_password_hash(default_password),
            role='super_admin',
        )
        db.session.add(user)
        db.session.commit()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
