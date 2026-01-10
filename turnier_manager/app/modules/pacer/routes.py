"""
PACEr Module - Routes
"""
from flask import render_template, request, jsonify, redirect, url_for, flash
from . import bp
from . import services
from ...models.calculation import TrackType
from ...models.tournament import Tournament


@bp.route('/pacer', methods=['GET'])
def calculator():
    """Show the PACEr calculator form"""
    tournaments = Tournament.query.order_by(Tournament.date.desc()).all()
    speed_options = services.get_speed_options()
    track_types = TrackType.CHOICES

    return render_template(
        'pages/pacer/calculator.html',
        tournaments=tournaments,
        speed_options=speed_options,
        track_types=track_types
    )


@bp.route('/pacer/calculate', methods=['POST'])
def calculate():
    """Process calculation and show results"""
    try:
        # Get form data
        distance = int(request.form.get('distance', 0))
        speed = float(request.form.get('speed', 0))
        track_type = request.form.get('track_type', TrackType.WEGSTRECKE)

        # Validate input
        if distance <= 0 or distance > 100000:
            flash('Distanz muss zwischen 1 und 100.000 Metern liegen.', 'error')
            return redirect(url_for('pacer.calculator'))

        if speed <= 0:
            flash('Geschwindigkeit muss größer als 0 sein.', 'error')
            return redirect(url_for('pacer.calculator'))

        # Calculate times
        times = services.calculate_pace(distance, speed, track_type)

        # Generate pace breakdown
        breakdown = services.generate_pace_breakdown(
            distance,
            times['bz_seconds'],
            times['ez_seconds'],
            times['hz_seconds']
        )

        # Format times for display
        result = {
            'distance_meters': distance,
            'distance_km': round(distance / 1000, 2),
            'speed_kmh': speed,
            'track_type': track_type,
            'track_type_label': dict(TrackType.CHOICES).get(track_type, track_type),
            'bz': services.format_time(times['bz_seconds']),
            'ez': services.format_time(times['ez_seconds']),
            'hz': services.format_time(times['hz_seconds']),
            'breakdown': breakdown
        }

        # Get tournaments for the share form
        tournaments = Tournament.query.order_by(Tournament.date.desc()).all()

        return render_template(
            'pages/pacer/result.html',
            result=result,
            times=times,
            tournaments=tournaments
        )

    except ValueError as e:
        flash(f'Ungültige Eingabe: {str(e)}', 'error')
        return redirect(url_for('pacer.calculator'))
    except Exception as e:
        flash('Ein Fehler ist aufgetreten. Bitte versuche es erneut.', 'error')
        return redirect(url_for('pacer.calculator'))


@bp.route('/pacer/save', methods=['POST'])
def save():
    """Save calculation to database (optionally public)"""
    try:
        # Get calculation data
        distance = int(request.form.get('distance', 0))
        speed = float(request.form.get('speed', 0))
        track_type = request.form.get('track_type', TrackType.WEGSTRECKE)
        bz_seconds = request.form.get('bz_seconds')
        ez_seconds = int(request.form.get('ez_seconds', 0))
        hz_seconds = int(request.form.get('hz_seconds', 0))

        # Optional metadata
        is_public = request.form.get('is_public') == 'on'
        tournament_id = request.form.get('tournament_id') or None
        class_name = request.form.get('class_name') or None
        test_name = request.form.get('test_name') or None
        notes = request.form.get('notes') or None

        if tournament_id:
            tournament_id = int(tournament_id)

        if bz_seconds:
            bz_seconds = int(bz_seconds)
        else:
            bz_seconds = None

        # Save to database
        calc = services.save_calculation(
            distance_meters=distance,
            speed_kmh=speed,
            track_type=track_type,
            bz_seconds=bz_seconds,
            ez_seconds=ez_seconds,
            hz_seconds=hz_seconds,
            is_public=is_public,
            tournament_id=tournament_id,
            class_name=class_name,
            test_name=test_name,
            notes=notes,
            ip_address=request.remote_addr
        )

        if is_public:
            flash('Berechnung wurde gespeichert und ist jetzt öffentlich sichtbar!', 'success')
            return redirect(url_for('history.index'))
        else:
            flash('Berechnung wurde gespeichert!', 'success')
            return redirect(url_for('pacer.calculator'))

    except Exception as e:
        flash(f'Fehler beim Speichern: {str(e)}', 'error')
        return redirect(url_for('pacer.calculator'))


@bp.route('/api/pacer/calculate', methods=['POST'])
def api_calculate():
    """API endpoint for AJAX calculations"""
    try:
        data = request.get_json()

        distance = int(data.get('distance', 0))
        speed = float(data.get('speed', 0))
        track_type = data.get('track_type', TrackType.WEGSTRECKE)

        if distance <= 0 or distance > 100000:
            return jsonify({'error': 'Invalid distance'}), 400

        if speed <= 0:
            return jsonify({'error': 'Invalid speed'}), 400

        times = services.calculate_pace(distance, speed, track_type)
        breakdown = services.generate_pace_breakdown(
            distance,
            times['bz_seconds'],
            times['ez_seconds'],
            times['hz_seconds']
        )

        return jsonify({
            'success': True,
            'distance_meters': distance,
            'distance_km': round(distance / 1000, 2),
            'speed_kmh': speed,
            'track_type': track_type,
            'bz': services.format_time(times['bz_seconds']),
            'ez': services.format_time(times['ez_seconds']),
            'hz': services.format_time(times['hz_seconds']),
            'breakdown': breakdown
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/pacer/speed-options/<track_type>')
def api_speed_options(track_type):
    """Get speed options for a specific track type"""
    options = services.get_speed_options(track_type)
    return jsonify(options)
