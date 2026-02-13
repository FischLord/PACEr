from flask import Blueprint, render_template, request
from datetime import date
from models import db, Report
from services.csrf import validate_csrf

bp_report = Blueprint('report', __name__)


@bp_report.route('/reportProblem', methods=['GET', 'POST'])
@validate_csrf
def report_problem():
    if request.method == 'POST':
        # Rate limiting: max 100 reports per day
        today = date.today()
        today_count = Report.query.filter(
            db.func.date(Report.created_at) == today
        ).count()

        if today_count >= 100:
            return render_template(
                'reportProblem.html',
                notification='Heute wurden bereits 100 Probleme gemeldet. Bitte versuchen Sie es morgen erneut.',
                notificationName='Warnung'
            )

        name = request.form.get('name', '')
        vorname = request.form.get('vorname', '')
        email = request.form.get('email', '')
        issue = request.form.get('issue', '')

        report = Report(name=name, vorname=vorname, email=email, issue=issue)
        db.session.add(report)
        db.session.commit()

        return render_template(
            'projektInfo.html',
            notification='Ihr Problem wurde erfolgreich gemeldet.',
            notificationName='Info'
        )

    return render_template('reportProblem.html')
