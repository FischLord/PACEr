"""
TurnierManager - Bug Report Model
"""
from datetime import datetime
from ..extensions import db


class ReportStatus:
    """Report status constants"""
    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    RESOLVED = 'resolved'

    CHOICES = [
        (OPEN, 'Offen'),
        (IN_PROGRESS, 'In Bearbeitung'),
        (RESOLVED, 'Gelöst')
    ]


class Report(db.Model):
    """Bug report model"""
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)

    # Reporter info
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=True)

    # Issue details
    issue_type = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=False)

    # Status tracking
    status = db.Column(db.String(20), default=ReportStatus.OPEN)
    admin_notes = db.Column(db.Text, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Report {self.id}: {self.status}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'issue_type': self.issue_type,
            'description': self.description,
            'status': self.status,
            'admin_notes': self.admin_notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
