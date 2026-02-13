import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Tournament, Calculation
from routes.admin import admin_required
from services.csrf import validate_csrf

bp_tournament = Blueprint('tournament', __name__)


# --- Public Routes ---

@bp_tournament.route('/turniere')
def turniere():
    tournaments = Tournament.query.filter_by(is_active=True).order_by(Tournament.datum.desc()).all()
    # Pre-parse klassen JSON for template
    for t in tournaments:
        t._klassen_list = json.loads(t.klassen) if t.klassen else []
    return render_template('tournaments/index.html', tournaments=tournaments)


@bp_tournament.route('/turnier/<int:tournament_id>')
def turnier_detail(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    klassen = json.loads(tournament.klassen) if tournament.klassen else []

    # Group calculations by klasse and parse results
    calculations = Calculation.query.filter_by(tournament_id=tournament_id).order_by(Calculation.created_at.desc()).all()
    calcs_by_klasse = {}
    for calc in calculations:
        # Parse result_json for template display
        if calc.result_json:
            parsed = json.loads(calc.result_json)
            calc._ez = parsed.get('ez', {})
            calc._hz = parsed.get('hz', {})
            calc._bz = parsed.get('bz', {})
            calc._has_bz = 'bz' in parsed
        else:
            calc._ez = {}
            calc._hz = {}
            calc._bz = {}
            calc._has_bz = False

        k = calc.klasse or 'Ohne Klasse'
        if k not in calcs_by_klasse:
            calcs_by_klasse[k] = []
        calcs_by_klasse[k].append(calc)

    return render_template(
        'tournaments/detail.html',
        tournament=tournament,
        klassen=klassen,
        calcs_by_klasse=calcs_by_klasse,
    )


# --- Admin Routes ---

@bp_tournament.route('/admin/turniere')
@admin_required
def admin_turniere():
    tournaments = Tournament.query.order_by(Tournament.datum.desc()).all()
    return render_template('admin/tournaments/list.html', tournaments=tournaments)


@bp_tournament.route('/admin/turnier/neu', methods=['GET', 'POST'])
@admin_required
@validate_csrf
def admin_turnier_neu():
    if request.method == 'POST':
        return _save_tournament()
    return render_template('admin/tournaments/form.html', tournament=None, existing_klassen=[])


@bp_tournament.route('/admin/turnier/<int:tournament_id>/bearbeiten', methods=['GET', 'POST'])
@admin_required
@validate_csrf
def admin_turnier_bearbeiten(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    if request.method == 'POST':
        return _save_tournament(tournament)
    existing_klassen = json.loads(tournament.klassen) if tournament.klassen else []
    return render_template('admin/tournaments/form.html', tournament=tournament, existing_klassen=existing_klassen)


@bp_tournament.route('/admin/turnier/<int:tournament_id>/loeschen', methods=['POST'])
@admin_required
@validate_csrf
def admin_turnier_loeschen(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    db.session.delete(tournament)
    db.session.commit()
    return redirect(url_for('tournament.admin_turniere'))


def _save_tournament(tournament=None):
    name = request.form.get('name', '').strip()
    datum_str = request.form.get('datum', '')
    ort = request.form.get('ort', '').strip()
    klassen = request.form.getlist('klassen')
    is_active = 'is_active' in request.form

    try:
        datum = datetime.strptime(datum_str, '%Y-%m-%d').date()
    except ValueError:
        existing_klassen = klassen
        return render_template(
            'admin/tournaments/form.html',
            tournament=tournament,
            existing_klassen=existing_klassen,
            notification='Ungültiges Datum',
            notificationName='Fehler'
        )

    if tournament is None:
        tournament = Tournament()
        db.session.add(tournament)

    tournament.name = name
    tournament.datum = datum
    tournament.ort = ort
    tournament.klassen = json.dumps(klassen)
    tournament.is_active = is_active

    db.session.commit()
    return redirect(url_for('tournament.admin_turniere'))
