"""
TurnierManager - Configuration
"""
import os
from pathlib import Path

basedir = Path(__file__).parent.parent


class Config:
    """Base configuration"""
    # Secret key from environment or generate one
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32).hex()

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{basedir / "turnier_manager.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Admin hash (set via environment variable)
    # Generate with: python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your_password'))"
    ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH')

    # App settings
    CALCULATIONS_PER_PAGE = 20
    MAX_DISTANCE_METERS = 100000  # 100km max


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
