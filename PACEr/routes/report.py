from flask import Blueprint, render_template, request
from datetime import date
from models import db, Report
from services.csrf import validate_csrf
from services.seo import page_meta

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
                notificationName='Warnung',
                **_feedback_meta(),
            )

        name = request.form.get('name', '')
        vorname = request.form.get('vorname', '')
        email = request.form.get('email', '')
        issue = request.form.get('issue', '')
        source = request.form.get('source', '').strip()
        if source:
            issue = f"{issue}\n\nGefunden ueber: {source}"

        report = Report(name=name, vorname=vorname, email=email, issue=issue)
        db.session.add(report)
        db.session.commit()

        return render_template(
            'projektInfo.html',
            notification='Ihr Problem wurde erfolgreich gemeldet.',
            notificationName='Info',
            **page_meta(
                title='PACEr - Fahrsport Marathon Zeitrechner',
                description='Berechne Bestzeit, erlaubte Zeit, Hoechstzeit und Kilometer-Splits fuer den Fahrsport-Marathon direkt am Handy.',
                canonical_path='/',
            ),
        )

    return render_template('reportProblem.html', **_feedback_meta())


def _feedback_meta():
    return page_meta(
        title='Feedback zu PACEr senden',
        description='Melde Fehler, unklare Berechnungen oder Verbesserungsvorschlaege zum PACEr Fahrsport-Rechner.',
        canonical_path='/reportProblem',
    )
