import json
from datetime import date
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, send_file
from helper import pace, calculatePace, oldPace, writeStatistics
from models import db, Calculation, Tournament
from services.pdf_generator import PacerPdfGenerator
from services.csrf import validate_csrf
from services.seo import page_meta
from services.tracking import record_referral_event

bp_calculator = Blueprint('calculator', __name__)

MAX_LENGTH = 100000


@bp_calculator.route('/rechner', methods=['GET', 'POST'])
@validate_csrf
def rechner():
    if request.method == 'POST':
        return _handle_calculation()

    record_referral_event('calculator_view')
    mode = request.args.get('mode', 'auto')
    selected_art = _get_followup_art(request.args.get('followup_after'))
    selected_tournament_id = request.args.get('tournament_id', '')
    selected_klasse = request.args.get('klasse', '')
    tournaments = Tournament.query.filter_by(is_active=True).filter(Tournament.datum >= date.today()).order_by(Tournament.datum.asc()).all()
    selected_klassen = _get_tournament_klassen(selected_tournament_id)
    return render_template(
        'calculator/rechner.html',
        mode=mode,
        has_result=False,
        tournaments=tournaments,
        selected_art=selected_art,
        selected_tournament_id=selected_tournament_id,
        selected_klasse=selected_klasse,
        selected_klassen=selected_klassen,
        show_ocr=False,
        **page_meta(
            title='Fahrsport Marathon Rechner - PACEr',
            description='Berechne BZ, EZ, HZ und Kilometer-Splits fuer Wegstrecke, Hindernisstrecke und Schrittstrecke.',
            canonical_path='/rechner',
        ),
    )


@bp_calculator.route('/pacer', methods=['GET', 'POST'])
@validate_csrf
def pacer():
    if request.method == 'POST':
        return _handle_calculation()
    return redirect(url_for('calculator.rechner'))


@bp_calculator.route('/pacerOld', methods=['GET', 'POST'])
@validate_csrf
def pacer_old():
    if request.method == 'POST':
        return _handle_calculation()
    return redirect(url_for('calculator.rechner', mode='manuell'))


@bp_calculator.route('/api/calculate', methods=['POST'])
@validate_csrf
def api_calculate():
    """HTMX endpoint — returns result partial."""
    return _handle_calculation(partial=True)


@bp_calculator.route('/api/calculations', methods=['POST'])
@validate_csrf
def api_calculations():
    """JSON endpoint for client-first calculations.

    The browser may render an immediate local result, but the server still
    recalculates and persists the calculation before returning PDF/follow-up
    URLs. This keeps stored tournament data authoritative.
    """
    try:
        template_vars = _calculate_and_save(request.form)
        return jsonify({
            'calculation_id': template_vars['calculation_id'],
            'pdf_url': url_for('calculator.export_pdf', calculation_id=template_vars['calculation_id']),
            'followup_form_url': template_vars['followup_form_url'],
        })
    except (ValueError, KeyError) as e:
        return jsonify({'error': f'Ungültige Eingabe: {e}'}), 400


@bp_calculator.route('/partials/form')
def partials_form():
    """Returns form partial for mode switching via HTMX."""
    mode = request.args.get('mode', 'auto')
    form_target_id = _get_form_target_id(request.args.get('target_id'))
    selected_tournament_id = request.args.get('tournament_id', '')
    selected_klasse = request.args.get('klasse', '')
    tournaments = Tournament.query.filter_by(is_active=True).filter(Tournament.datum >= date.today()).order_by(Tournament.datum.asc()).all()
    template = 'partials/form_old.html' if mode == 'manuell' else 'partials/form_new.html'
    return render_template(
        template,
        use_htmx=True,
        tournaments=tournaments,
        selected_art=_get_followup_art(request.args.get('followup_after')),
        selected_tournament_id=selected_tournament_id,
        selected_klasse=selected_klasse,
        selected_klassen=_get_tournament_klassen(selected_tournament_id),
        form_target_id=form_target_id,
        reset_form_url=_build_partial_form_url(
            mode=mode,
            followup_after=request.args.get('followup_after'),
            target_id=form_target_id,
            tournament_id=selected_tournament_id,
            klasse=selected_klasse,
        ),
    )


@bp_calculator.route('/api/tournament-klassen')
def api_tournament_klassen():
    """Returns klasse select partial for a given tournament."""
    tournament_id = request.args.get('tournament_id')
    if not tournament_id:
        return ''
    tournament = Tournament.query.get(tournament_id)
    if not tournament:
        return ''
    klassen = json.loads(tournament.klassen) if tournament.klassen else []
    return render_template(
        'partials/klasse_select.html',
        klassen=klassen,
        selected_klasse='',
        form_target_id=_get_form_target_id(request.args.get('target_id')),
    )


def _get_followup_art(previous_art):
    """Preselect the next likely section without forcing a combined workflow."""
    if previous_art == 'wegstrecke':
        return 'hindernisstrecke'
    return None


def _get_tournament_klassen(tournament_id):
    if not tournament_id:
        return []
    tournament = Tournament.query.get(tournament_id)
    if not tournament or not tournament.klassen:
        return []
    return json.loads(tournament.klassen)


def _get_form_target_id(target_id):
    if target_id and target_id.replace('-', '').isalnum():
        return target_id
    return 'form-area'


@bp_calculator.route('/api/export/pdf/<int:calculation_id>')
def export_pdf(calculation_id):
    """Generate and download PDF for a calculation."""
    calc = Calculation.query.get_or_404(calculation_id)
    record_referral_event('pdf_export', path='/api/export/pdf')
    generator = PacerPdfGenerator(calc)
    pdf_buffer = generator.generate()

    filename = f'pacer_{calc.laenge}m'
    if calc.art:
        filename += f'_{calc.art}'
    filename += '.pdf'

    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename,
    )


@bp_calculator.route('/api/ocr', methods=['POST'])
@validate_csrf
def api_ocr():
    """Analyze uploaded photo and return pre-filled form partial."""
    from services.ocr_service import get_ocr_service

    if 'photo' not in request.files:
        return render_template('partials/error.html', error='Kein Foto hochgeladen.')

    file = request.files['photo']
    if not file.filename:
        return render_template('partials/error.html', error='Kein Foto ausgewählt.')

    image_data = file.read()
    mime_type = file.content_type or 'image/jpeg'

    service = get_ocr_service()
    if not service:
        return render_template('partials/error.html',
                               error='OCR-Service nicht verfügbar. Bitte ANTHROPIC_API_KEY setzen oder Tesseract installieren.')

    result = service.analyze(image_data, mime_type)
    if not result:
        return render_template('partials/error.html', error='Foto konnte nicht analysiert werden.')

    return render_template('partials/ocr_result.html', ocr=result)


def _handle_calculation(partial=False):
    """Core calculation handler for all modes."""
    try:
        mode = request.form.get('mode', 'auto')
        template_vars = _calculate_and_save(request.form)

        if partial:
            return render_template('partials/results.html', **template_vars)

        return render_template(
            'calculator/rechner.html',
            mode=mode, has_result=True,
            **template_vars,
        )

    except (ValueError, KeyError) as e:
        error = f"Ungültige Eingabe: {e}"
        if partial:
            return render_template('partials/error.html', error=error)
        return render_template(
            'calculator/rechner.html', mode=request.form.get('mode', 'auto'),
            has_result=False, notification=error, notificationName='Fehler',
            tournaments=Tournament.query.filter_by(is_active=True).filter(Tournament.datum >= date.today()).order_by(Tournament.datum.asc()).all(),
        )


def _calculate_and_save(form_data):
    mode = form_data.get('mode', 'auto')
    laenge = int(form_data['laenge'])

    if laenge <= 0 or laenge > MAX_LENGTH:
        raise ValueError(f"Bitte eine Streckenlänge zwischen 1 und {MAX_LENGTH} m angeben.")

    if mode == 'manuell':
        bz_min = int(form_data['bz_min'])
        bz_sec = int(form_data['bz_sec'])
        ez_min = int(form_data['ez_min'])
        ez_sec = int(form_data['ez_sec'])
        hz_min = int(form_data['hz_min'])
        hz_sec = int(form_data['hz_sec'])

        ez_result = pace(laenge, ez_min, ez_sec)
        hz_result = pace(laenge, hz_min, hz_sec)
        bz_result = pace(laenge, bz_min, bz_sec)

        art = None
        kmh = None
    else:
        kmh = int(form_data['kmh'])
        art = form_data['art']

        bz_sec, hz_sec, ez_sec, bz_min, hz_min, ez_min = calculatePace(laenge, kmh, art)
        ez_result = pace(laenge, ez_min, ez_sec)
        hz_result = pace(laenge, hz_min, hz_sec)
        bz_result = pace(laenge, bz_min, bz_sec) if bz_min is not None else None

    writeStatistics()

    result_data = {
        'ez': {str(k): v for k, v in ez_result.items()},
        'hz': {str(k): v for k, v in hz_result.items()},
    }
    if bz_result:
        result_data['bz'] = {str(k): v for k, v in bz_result.items()}

    calc = Calculation(
        laenge=laenge,
        art=art,
        kmh=kmh,
        bz_min=bz_min, bz_sec=bz_sec,
        ez_min=ez_min, ez_sec=ez_sec,
        hz_min=hz_min, hz_sec=hz_sec,
        result_json=json.dumps(result_data),
        mode=mode,
    )

    tournament_id = form_data.get('tournament_id')
    if tournament_id:
        calc.tournament_id = int(tournament_id)
        calc.klasse = form_data.get('klasse', '')

    db.session.add(calc)
    db.session.commit()
    record_referral_event('calculation')

    return dict(
        laenge=laenge, kmh=kmh, art=art,
        bz_result=bz_result, ez_result=ez_result, hz_result=hz_result,
        calculation_id=calc.id,
        followup_form_url=_build_followup_form_url(calc),
    )


def _build_followup_form_url(calc):
    if not calc.art:
        return None

    return _build_partial_form_url(
        mode='auto',
        followup_after=calc.art,
        target_id=f'followup-slot-{calc.id}',
        tournament_id=calc.tournament_id,
        klasse=calc.klasse,
    )


def _build_partial_form_url(mode='auto', followup_after=None, target_id='form-area', tournament_id=None, klasse=None):
    params = {
        'mode': mode,
        'target_id': target_id,
    }
    if followup_after:
        params['followup_after'] = followup_after
    if tournament_id:
        params['tournament_id'] = tournament_id
    if klasse:
        params['klasse'] = klasse
    return url_for('calculator.partials_form', **params)
