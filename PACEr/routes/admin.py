from functools import wraps
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User, Report
from services.csrf import validate_csrf
from services.rate_limit import check_rate_limit, record_attempt

bp_admin = Blueprint('admin', __name__)


def admin_required(f):
    """Backward-compatible decorator — delegates to Flask-Login."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function


@bp_admin.route('/adminLogin', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_tools'))

    if request.method == 'POST':
        # CSRF check
        token = request.form.get('_csrf_token') or request.headers.get('X-CSRFToken')
        if not token or token != session.get('_csrf_token'):
            return render_template(
                'admin/adminLogin.html',
                notification='Ungueltige Anfrage.',
                notificationName='Fehler'
            )

        ip = request.remote_addr
        if check_rate_limit(ip):
            return render_template(
                'admin/adminLogin.html',
                notification='Zu viele Fehlversuche. Bitte in 5 Minuten erneut versuchen.',
                notificationName='Warnung'
            )

        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            try:
                user.last_login = datetime.utcnow()
                db.session.commit()
            except Exception:
                db.session.rollback()
            session.permanent = True
            login_user(user)
            return redirect(url_for('admin.admin_tools'))

        record_attempt(ip)
        return render_template(
            'admin/adminLogin.html',
            notification='Falscher Benutzername oder Passwort.',
            notificationName='Warnung'
        )

    return render_template('admin/adminLogin.html')


@bp_admin.route('/adminLogout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin.admin_login'))


@bp_admin.route('/adminTools')
@admin_required
def admin_tools():
    return render_template('admin/adminTools.html')


@bp_admin.route('/changePassword', methods=['GET', 'POST'])
@admin_required
@validate_csrf
def change_password():
    if request.method == 'POST':
        current_pw = request.form.get('current_password', '')
        new_pw = request.form.get('new_password', '')
        confirm_pw = request.form.get('confirm_password', '')

        if not check_password_hash(current_user.password_hash, current_pw):
            return render_template(
                'admin/changePassword.html',
                notification='Aktuelles Passwort ist falsch.',
                notificationName='Fehler'
            )

        if len(new_pw) < 8:
            return render_template(
                'admin/changePassword.html',
                notification='Neues Passwort muss mindestens 8 Zeichen lang sein.',
                notificationName='Fehler'
            )

        if new_pw != confirm_pw:
            return render_template(
                'admin/changePassword.html',
                notification='Passwoerter stimmen nicht ueberein.',
                notificationName='Fehler'
            )

        current_user.password_hash = generate_password_hash(new_pw)
        db.session.commit()

        return render_template(
            'admin/changePassword.html',
            notification='Passwort erfolgreich geaendert.',
            notificationName='Erfolg'
        )

    return render_template('admin/changePassword.html')


@bp_admin.route('/viewReports')
@admin_required
def view_reports():
    reports = Report.query.order_by(Report.created_at.desc()).all()
    return render_template('admin/viewReports.html', reports=reports)


@bp_admin.route('/displayReport/<int:report_id>')
@admin_required
def display_report(report_id):
    report = Report.query.get_or_404(report_id)
    return render_template('admin/displayReport.html', report=report)
