"""
TurnierManager - Main Routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models.calculation import Calculation
from .models.tournament import Tournament
from .models.report import Report
from .extensions import db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Homepage - shows PACEr quick access and recent public calculations"""
    # Get recent public calculations
    recent_calculations = Calculation.query.filter_by(is_public=True).order_by(
        Calculation.created_at.desc()
    ).limit(5).all()

    # Get active tournaments (future or recent)
    from datetime import datetime, timedelta
    cutoff = datetime.utcnow().date() - timedelta(days=30)
    active_tournaments = Tournament.query.filter(
        (Tournament.date >= cutoff) | (Tournament.date.is_(None))
    ).order_by(Tournament.date.desc()).limit(5).all()

    return render_template(
        'pages/home.html',
        recent_calculations=recent_calculations,
        active_tournaments=active_tournaments
    )


@bp.route('/info')
def info():
    """Project info page - explains what TurnierManager/PACEr does"""
    return render_template('pages/info.html')


@bp.route('/about')
def about():
    """About page"""
    return render_template('pages/about.html')


@bp.route('/impressum')
def impressum():
    """Legal page / Impressum"""
    return render_template('pages/impressum.html')


@bp.route('/report', methods=['GET', 'POST'])
def report_problem():
    """Bug report submission"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        issue_type = request.form.get('issue_type', '').strip()
        description = request.form.get('description', '').strip()

        if not name or not description:
            flash('Name und Beschreibung sind erforderlich.', 'error')
            return render_template('pages/report.html')

        report = Report(
            name=name,
            email=email if email else None,
            issue_type=issue_type if issue_type else None,
            description=description
        )
        db.session.add(report)
        db.session.commit()

        flash('Danke für dein Feedback! Wir werden uns darum kümmern.', 'success')
        return redirect(url_for('main.index'))

    return render_template('pages/report.html')
