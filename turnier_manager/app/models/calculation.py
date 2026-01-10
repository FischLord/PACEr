"""
TurnierManager - Calculation Model (PACEr)
"""
from datetime import datetime
from ..extensions import db


class TrackType:
    """Track type constants"""
    WEGSTRECKE = 'wegstrecke'
    HINDERNISSTRECKE = 'hindernisstrecke'
    SCHRITTSTRECKE = 'schrittstrecke'

    CHOICES = [
        (WEGSTRECKE, 'Wegstrecke'),
        (HINDERNISSTRECKE, 'Hindernisstrecke'),
        (SCHRITTSTRECKE, 'Schrittstrecke')
    ]


class Calculation(db.Model):
    """Pace calculation model"""
    __tablename__ = 'calculations'

    id = db.Column(db.Integer, primary_key=True)

    # Tournament reference (optional)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=True)

    # Input values
    distance_meters = db.Column(db.Integer, nullable=False)
    speed_kmh = db.Column(db.Float, nullable=True)  # NULL for manual time input
    track_type = db.Column(db.String(20), nullable=False, default=TrackType.WEGSTRECKE)

    # Calculated times (in seconds for precision)
    bz_seconds = db.Column(db.Integer, nullable=True)  # Bestzeit
    ez_seconds = db.Column(db.Integer, nullable=False)  # Erlaubte Zeit
    hz_seconds = db.Column(db.Integer, nullable=False)  # Höchstzeit

    # Metadata for public history
    class_name = db.Column(db.String(50), nullable=True)  # z.B. "M", "S", "A"
    test_name = db.Column(db.String(100), nullable=True)  # z.B. "Marathon A"
    notes = db.Column(db.Text, nullable=True)

    # Visibility
    is_public = db.Column(db.Boolean, default=False)

    # Timestamps and tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_hash = db.Column(db.String(64), nullable=True)  # Anonymized for spam protection

    def __repr__(self):
        return f'<Calculation {self.id}: {self.distance_meters}m @ {self.track_type}>'

    @property
    def bz_formatted(self):
        """Return Bestzeit as MM:SS string"""
        if self.bz_seconds is None:
            return None
        mins, secs = divmod(self.bz_seconds, 60)
        return f'{mins}:{secs:02d}'

    @property
    def ez_formatted(self):
        """Return Erlaubte Zeit as MM:SS string"""
        mins, secs = divmod(self.ez_seconds, 60)
        return f'{mins}:{secs:02d}'

    @property
    def hz_formatted(self):
        """Return Höchstzeit as MM:SS string"""
        mins, secs = divmod(self.hz_seconds, 60)
        return f'{mins}:{secs:02d}'

    @property
    def distance_km(self):
        """Return distance in kilometers"""
        return self.distance_meters / 1000

    def to_dict(self):
        """Convert to dictionary for JSON/API responses"""
        return {
            'id': self.id,
            'tournament_id': self.tournament_id,
            'tournament_name': self.tournament.name if self.tournament else None,
            'distance_meters': self.distance_meters,
            'distance_km': self.distance_km,
            'speed_kmh': self.speed_kmh,
            'track_type': self.track_type,
            'bz': self.bz_formatted,
            'ez': self.ez_formatted,
            'hz': self.hz_formatted,
            'bz_seconds': self.bz_seconds,
            'ez_seconds': self.ez_seconds,
            'hz_seconds': self.hz_seconds,
            'class_name': self.class_name,
            'test_name': self.test_name,
            'notes': self.notes,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat()
        }

    def generate_pace_breakdown(self):
        """Generate per-km pace breakdown for all time types"""
        breakdown = {
            'ez': self._calculate_pace_per_km(self.ez_seconds),
            'hz': self._calculate_pace_per_km(self.hz_seconds)
        }
        if self.bz_seconds:
            breakdown['bz'] = self._calculate_pace_per_km(self.bz_seconds)
        return breakdown

    def _calculate_pace_per_km(self, total_seconds):
        """Calculate time at each km mark"""
        if not total_seconds or self.distance_meters <= 0:
            return []

        pace_per_meter = total_seconds / self.distance_meters
        result = []
        km = 1
        while km * 1000 <= self.distance_meters:
            time_at_km = int(km * 1000 * pace_per_meter)
            mins, secs = divmod(time_at_km, 60)
            result.append({
                'km': km,
                'time_seconds': time_at_km,
                'time_formatted': f'{mins}:{secs:02d}'
            })
            km += 1

        # Add final distance if not exact km
        if self.distance_meters % 1000 != 0:
            result.append({
                'km': self.distance_km,
                'time_seconds': total_seconds,
                'time_formatted': self._format_time(total_seconds)
            })

        return result

    @staticmethod
    def _format_time(seconds):
        mins, secs = divmod(seconds, 60)
        return f'{mins}:{secs:02d}'
