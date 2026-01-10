"""
TurnierManager - Flask Application Factory
"""
from flask import Flask
from .extensions import db, migrate
from .config import Config


def create_app(config_class=Config):
    """Application Factory Pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .modules.pacer import bp as pacer_bp
    from .modules.history import bp as history_bp
    from .modules.admin import bp as admin_bp
    from .modules.auth import bp as auth_bp

    app.register_blueprint(pacer_bp)
    app.register_blueprint(history_bp, url_prefix='/verlauf')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Register main routes
    from . import routes
    app.register_blueprint(routes.bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
