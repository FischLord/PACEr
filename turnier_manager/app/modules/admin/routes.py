"""
Admin Module - Routes
"""
from functools import wraps
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from . import bp
from ...models.calculation import Calculation
from ...models.tournament import Tournament
from ...models.report import Report, ReportStatus
from ...extensions import db
from datetime import datetime, timedelta
from sqlalchemy import func


def admin_required(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Bitte zuerst anmelden.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/')
@admin_required
def dashboard():
    """Admin dashboard with statistics"""
    # Calculate statistics
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    stats = {
        'total_calculations': Calculation.query.count(),
        'public_calculations': Calculation.query.filter_by(is_public=True).count(),
        'calculations_today': Calculation.query.filter(
            func.date(Calculation.created_at) == today
        ).count(),
        'calculations_week': Calculation.query.filter(
            Calculation.created_at >= week_ago
        ).count(),
        'calculations_month': Calculation.query.filter(
            Calculation.created_at >= month_ago
        ).count(),
        'total_tournaments': Tournament.query.count(),
        'open_reports': Report.query.filter_by(status=ReportStatus.OPEN).count(),
    }

    # Recent calculations
    recent_calculations = Calculation.query.order_by(
        Calculation.created_at.desc()
    ).limit(10).all()

    # Recent reports
    recent_reports = Report.query.order_by(
        Report.created_at.desc()
    ).limit(5).all()

    return render_template(
        'pages/admin/dashboard.html',
        stats=stats,
        recent_calculations=recent_calculations,
        recent_reports=recent_reports
    )


# ============ Calculations Management ============

@bp.route('/calculations')
@admin_required
def calculations():
    """List all calculations"""
    page = request.args.get('page', 1, type=int)
    only_public = request.args.get('public', False, type=bool)

    query = Calculation.query
    if only_public:
        query = query.filter_by(is_public=True)

    pagination = query.order_by(Calculation.created_at.desc()).paginate(
        page=page, per_page=50, error_out=False
    )

    return render_template(
        'pages/admin/calculations.html',
        calculations=pagination.items,
        pagination=pagination
    )


@bp.route('/calculations/<int:calc_id>/delete', methods=['POST'])
@admin_required
def delete_calculation(calc_id):
    """Delete a calculation"""
    calc = Calculation.query.get_or_404(calc_id)
    db.session.delete(calc)
    db.session.commit()
    flash('Berechnung gelöscht.', 'success')
    return redirect(url_for('admin.calculations'))


@bp.route('/calculations/<int:calc_id>/toggle-public', methods=['POST'])
@admin_required
def toggle_calculation_public(calc_id):
    """Toggle public visibility of a calculation"""
    calc = Calculation.query.get_or_404(calc_id)
    calc.is_public = not calc.is_public
    db.session.commit()

    status = 'öffentlich' if calc.is_public else 'privat'
    flash(f'Berechnung ist jetzt {status}.', 'success')
    return redirect(url_for('admin.calculations'))


# ============ Tournament Management ============

@bp.route('/tournaments')
@admin_required
def tournaments():
    """List all tournaments"""
    tournaments = Tournament.query.order_by(Tournament.date.desc()).all()
    return render_template('pages/admin/tournaments.html', tournaments=tournaments)


@bp.route('/tournaments/new', methods=['GET', 'POST'])
@admin_required
def new_tournament():
    """Create a new tournament"""
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        date_str = request.form.get('date')

        if not name:
            flash('Name ist erforderlich.', 'error')
            return render_template('pages/admin/tournament_form.html')

        tournament = Tournament(
            name=name,
            location=location,
            date=datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
        )
        db.session.add(tournament)
        db.session.commit()

        flash('Turnier erstellt.', 'success')
        return redirect(url_for('admin.tournaments'))

    return render_template('pages/admin/tournament_form.html')


@bp.route('/tournaments/<int:tournament_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_tournament(tournament_id):
    """Edit a tournament"""
    tournament = Tournament.query.get_or_404(tournament_id)

    if request.method == 'POST':
        tournament.name = request.form.get('name')
        tournament.location = request.form.get('location')
        date_str = request.form.get('date')
        tournament.date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        db.session.commit()
        flash('Turnier aktualisiert.', 'success')
        return redirect(url_for('admin.tournaments'))

    return render_template('pages/admin/tournament_form.html', tournament=tournament)


@bp.route('/tournaments/<int:tournament_id>/delete', methods=['POST'])
@admin_required
def delete_tournament(tournament_id):
    """Delete a tournament"""
    tournament = Tournament.query.get_or_404(tournament_id)

    # Check for associated calculations
    if tournament.calculations.count() > 0:
        flash('Turnier kann nicht gelöscht werden, da noch Berechnungen zugeordnet sind.', 'error')
        return redirect(url_for('admin.tournaments'))

    db.session.delete(tournament)
    db.session.commit()
    flash('Turnier gelöscht.', 'success')
    return redirect(url_for('admin.tournaments'))


# ============ Reports Management ============

@bp.route('/reports')
@admin_required
def reports():
    """List all bug reports"""
    status_filter = request.args.get('status')

    query = Report.query
    if status_filter:
        query = query.filter_by(status=status_filter)

    reports = query.order_by(Report.created_at.desc()).all()
    statuses = ReportStatus.CHOICES

    return render_template(
        'pages/admin/reports.html',
        reports=reports,
        statuses=statuses,
        current_status=status_filter
    )


@bp.route('/reports/<int:report_id>')
@admin_required
def view_report(report_id):
    """View a single report"""
    report = Report.query.get_or_404(report_id)
    statuses = ReportStatus.CHOICES
    return render_template('pages/admin/report_detail.html', report=report, statuses=statuses)


@bp.route('/reports/<int:report_id>/update', methods=['POST'])
@admin_required
def update_report(report_id):
    """Update report status and notes"""
    report = Report.query.get_or_404(report_id)

    report.status = request.form.get('status', report.status)
    report.admin_notes = request.form.get('admin_notes')

    db.session.commit()
    flash('Report aktualisiert.', 'success')
    return redirect(url_for('admin.view_report', report_id=report_id))


@bp.route('/reports/<int:report_id>/delete', methods=['POST'])
@admin_required
def delete_report(report_id):
    """Delete a report"""
    report = Report.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    flash('Report gelöscht.', 'success')
    return redirect(url_for('admin.reports'))
