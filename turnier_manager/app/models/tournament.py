"""
TurnierManager - Tournament Model
"""
from datetime import datetime
from ..extensions import db


class Tournament(db.Model):
    """Tournament/Veranstaltung model"""
    __tablename__ = 'tournaments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to calculations
    calculations = db.relationship('Calculation', backref='tournament', lazy='dynamic')

    def __repr__(self):
        return f'<Tournament {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'date': self.date.isoformat() if self.date else None,
            'created_at': self.created_at.isoformat()
        }
