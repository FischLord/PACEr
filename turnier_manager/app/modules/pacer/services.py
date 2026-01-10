"""
PACEr Module - Business Logic / Services
"""
from ...models.calculation import Calculation, TrackType
from ...extensions import db
import hashlib


def calculate_pace(distance_meters: int, speed_kmh: float, track_type: str) -> dict:
    """
    Calculate BZ, EZ, HZ times based on distance, speed and track type.

    Args:
        distance_meters: Distance in meters
        speed_kmh: Speed in km/h
        track_type: One of 'wegstrecke', 'hindernisstrecke', 'schrittstrecke'

    Returns:
        Dictionary with calculated times in seconds
    """
    # Convert meters to km
    distance_km = distance_meters / 1000

    # Calculate EZ (Erlaubte Zeit) in seconds
    # Formula: (distance_km * 60 / speed_kmh) * 60 = seconds
    ez_seconds = int((distance_km * 60 / speed_kmh) * 60)

    # Calculate HZ and BZ based on track type
    if track_type == TrackType.WEGSTRECKE:
        hz_seconds = int(ez_seconds * 1.2)
        bz_seconds = ez_seconds - 120  # 2 minutes less
    elif track_type == TrackType.HINDERNISSTRECKE:
        hz_seconds = int(ez_seconds * 2)
        bz_seconds = ez_seconds - 180  # 3 minutes less
    elif track_type == TrackType.SCHRITTSTRECKE:
        hz_seconds = int(ez_seconds * 2)
        bz_seconds = None  # No Bestzeit for Schrittstrecke
    else:
        raise ValueError(f"Unknown track type: {track_type}")

    # Ensure BZ is not negative
    if bz_seconds is not None and bz_seconds < 0:
        bz_seconds = 0

    return {
        'bz_seconds': bz_seconds,
        'ez_seconds': ez_seconds,
        'hz_seconds': hz_seconds
    }


def format_time(seconds: int) -> dict:
    """Convert seconds to minutes and seconds dict"""
    if seconds is None:
        return {'minutes': None, 'seconds': None, 'formatted': None}
    mins, secs = divmod(seconds, 60)
    return {
        'minutes': mins,
        'seconds': secs,
        'formatted': f'{mins}:{secs:02d}'
    }


def generate_pace_breakdown(distance_meters: int, bz_seconds: int, ez_seconds: int, hz_seconds: int) -> dict:
    """
    Generate per-km pace breakdown for all time types.

    Returns dict with 'bz', 'ez', 'hz' keys, each containing list of km breakdowns
    """
    result = {
        'ez': _calculate_km_breakdown(distance_meters, ez_seconds),
        'hz': _calculate_km_breakdown(distance_meters, hz_seconds)
    }

    if bz_seconds is not None:
        result['bz'] = _calculate_km_breakdown(distance_meters, bz_seconds)

    return result


def _calculate_km_breakdown(distance_meters: int, total_seconds: int) -> list:
    """Calculate time at each km mark"""
    if not total_seconds or distance_meters <= 0:
        return []

    pace_per_meter = total_seconds / distance_meters
    result = []
    km = 1

    while km * 1000 <= distance_meters:
        time_at_km = int(km * 1000 * pace_per_meter)
        mins, secs = divmod(time_at_km, 60)
        result.append({
            'distance_m': km * 1000,
            'distance_km': km,
            'time_seconds': time_at_km,
            'time_formatted': f'{mins}:{secs:02d}'
        })
        km += 1

    # Add final distance if not exact km
    if distance_meters % 1000 != 0:
        mins, secs = divmod(total_seconds, 60)
        result.append({
            'distance_m': distance_meters,
            'distance_km': round(distance_meters / 1000, 2),
            'time_seconds': total_seconds,
            'time_formatted': f'{mins}:{secs:02d}'
        })

    return result


def save_calculation(
    distance_meters: int,
    speed_kmh: float,
    track_type: str,
    bz_seconds: int,
    ez_seconds: int,
    hz_seconds: int,
    is_public: bool = False,
    tournament_id: int = None,
    class_name: str = None,
    test_name: str = None,
    notes: str = None,
    ip_address: str = None
) -> Calculation:
    """
    Save a calculation to the database.

    Returns the created Calculation object.
    """
    # Hash IP for spam protection (anonymized)
    ip_hash = None
    if ip_address:
        ip_hash = hashlib.sha256(ip_address.encode()).hexdigest()[:16]

    calc = Calculation(
        distance_meters=distance_meters,
        speed_kmh=speed_kmh,
        track_type=track_type,
        bz_seconds=bz_seconds,
        ez_seconds=ez_seconds,
        hz_seconds=hz_seconds,
        is_public=is_public,
        tournament_id=tournament_id,
        class_name=class_name,
        test_name=test_name,
        notes=notes,
        ip_hash=ip_hash
    )

    db.session.add(calc)
    db.session.commit()

    return calc


def get_public_calculations(page: int = 1, per_page: int = 20, tournament_id: int = None):
    """
    Get paginated list of public calculations.

    Returns pagination object.
    """
    query = Calculation.query.filter_by(is_public=True)

    if tournament_id:
        query = query.filter_by(tournament_id=tournament_id)

    return query.order_by(Calculation.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )


def get_calculation_by_id(calc_id: int) -> Calculation:
    """Get a single calculation by ID"""
    return Calculation.query.get(calc_id)


# Speed options per track type (for dropdown)
SPEED_OPTIONS = {
    TrackType.WEGSTRECKE: [
        {'value': 12, 'label': '12 km/h'},
        {'value': 13, 'label': '13 km/h'},
        {'value': 14, 'label': '14 km/h'},
        {'value': 15, 'label': '15 km/h'},
    ],
    TrackType.HINDERNISSTRECKE: [
        {'value': 12, 'label': '12 km/h'},
        {'value': 13, 'label': '13 km/h'},
        {'value': 14, 'label': '14 km/h'},
        {'value': 15, 'label': '15 km/h'},
    ],
    TrackType.SCHRITTSTRECKE: [
        {'value': 6, 'label': '6 km/h'},
        {'value': 7, 'label': '7 km/h'},
    ]
}


def get_speed_options(track_type: str = None) -> dict:
    """Get speed options for dropdown, optionally filtered by track type"""
    if track_type:
        return SPEED_OPTIONS.get(track_type, [])
    return SPEED_OPTIONS
