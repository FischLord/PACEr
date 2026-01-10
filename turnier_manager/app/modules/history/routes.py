"""
History Module - Routes for Public Calculation History
"""
from flask import render_template, request, jsonify
from . import bp
from ...models.calculation import Calculation, TrackType
from ...models.tournament import Tournament
from flask import current_app


@bp.route('/')
def index():
    """Show public calculation history"""
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('CALCULATIONS_PER_PAGE', 20)

    # Filters
    tournament_id = request.args.get('tournament_id', type=int)
    track_type = request.args.get('track_type')
    class_name = request.args.get('class_name')

    # Build query
    query = Calculation.query.filter_by(is_public=True)

    if tournament_id:
        query = query.filter_by(tournament_id=tournament_id)
    if track_type:
        query = query.filter_by(track_type=track_type)
    if class_name:
        query = query.filter_by(class_name=class_name)

    # Get paginated results
    pagination = query.order_by(Calculation.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Get filter options
    tournaments = Tournament.query.order_by(Tournament.date.desc()).all()
    track_types = TrackType.CHOICES

    # Get unique class names
    class_names = [c[0] for c in Calculation.query.with_entities(
        Calculation.class_name
    ).filter(
        Calculation.is_public == True,
        Calculation.class_name.isnot(None)
    ).distinct().all()]

    return render_template(
        'pages/history/index.html',
        calculations=pagination.items,
        pagination=pagination,
        tournaments=tournaments,
        track_types=track_types,
        class_names=class_names,
        current_filters={
            'tournament_id': tournament_id,
            'track_type': track_type,
            'class_name': class_name
        }
    )


@bp.route('/<int:calc_id>')
def detail(calc_id):
    """Show single calculation detail"""
    calc = Calculation.query.filter_by(id=calc_id, is_public=True).first_or_404()

    # Generate breakdown
    breakdown = calc.generate_pace_breakdown()

    return render_template(
        'pages/history/detail.html',
        calculation=calc,
        breakdown=breakdown
    )


@bp.route('/turnier/<int:tournament_id>')
def by_tournament(tournament_id):
    """Show all calculations for a specific tournament"""
    tournament = Tournament.query.get_or_404(tournament_id)

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('CALCULATIONS_PER_PAGE', 20)

    pagination = Calculation.query.filter_by(
        is_public=True,
        tournament_id=tournament_id
    ).order_by(Calculation.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template(
        'pages/history/tournament.html',
        tournament=tournament,
        calculations=pagination.items,
        pagination=pagination
    )


@bp.route('/api/search')
def api_search():
    """API endpoint for searching calculations"""
    query = request.args.get('q', '')
    limit = request.args.get('limit', 10, type=int)

    if len(query) < 2:
        return jsonify([])

    # Search in tournament names, class names, test names
    results = Calculation.query.filter(
        Calculation.is_public == True
    ).join(
        Tournament, Calculation.tournament_id == Tournament.id, isouter=True
    ).filter(
        (Tournament.name.ilike(f'%{query}%')) |
        (Calculation.class_name.ilike(f'%{query}%')) |
        (Calculation.test_name.ilike(f'%{query}%'))
    ).limit(limit).all()

    return jsonify([calc.to_dict() for calc in results])
