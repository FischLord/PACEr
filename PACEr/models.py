from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='super_admin')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)


class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    vorname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    issue = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class UsageStatistic(db.Model):
    __tablename__ = 'usage_statistics'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    count = db.Column(db.Integer, default=1)


class Calculation(db.Model):
    __tablename__ = 'calculations'
    id = db.Column(db.Integer, primary_key=True)
    laenge = db.Column(db.Integer, nullable=False)
    art = db.Column(db.String(50))
    kmh = db.Column(db.Integer)
    bz_min = db.Column(db.Integer)
    bz_sec = db.Column(db.Integer)
    ez_min = db.Column(db.Integer)
    ez_sec = db.Column(db.Integer)
    hz_min = db.Column(db.Integer)
    hz_sec = db.Column(db.Integer)
    result_json = db.Column(db.Text)
    mode = db.Column(db.String(20))  # 'auto' or 'manuell'
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=True)
    klasse = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tournament = db.relationship('Tournament', backref=db.backref('calculations', lazy=True))


class Tournament(db.Model):
    __tablename__ = 'tournaments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    datum = db.Column(db.Date, nullable=False)
    ort = db.Column(db.String(200), nullable=False)
    klassen = db.Column(db.Text, default='[]')  # JSON string
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AdminConfig(db.Model):
    __tablename__ = 'admin_config'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
