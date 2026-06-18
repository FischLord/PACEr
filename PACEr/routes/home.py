from datetime import date
import os

from flask import Blueprint, Response, current_app, render_template, request, url_for

from models import Tournament
from services.seo import page_meta, webapp_schema
from services.tracking import record_referral_event

bp_home = Blueprint('home', __name__)


@bp_home.route('/')
def index():
    try:
        record_referral_event('landing_view')
        return render_template(
            'projektInfo.html',
            structured_data=webapp_schema(request.url_root),
            **page_meta(
                title='PACEr - Fahrsport Marathon Zeitrechner',
                description='Berechne Bestzeit, erlaubte Zeit, Hoechstzeit und Kilometer-Splits fuer den Fahrsport-Marathon direkt am Handy.',
                canonical_path='/',
            ),
        )

    except Exception as e:
        return 'Error: ' + str(e)


@bp_home.route('/aboutUs')
def aboutUs():
    try:
        return render_template(
            'aboutUs.html',
            **page_meta(
                title='Ueber PACEr und Janneck Lehmann',
                description='Wer hinter PACEr steht: Janneck Lehmann, Fahrsportler und Entwickler des Marathon-Zeitrechners.',
                canonical_path='/aboutUs',
            ),
        )

    except Exception as e:
        return 'Error: ' + str(e)


@bp_home.route('/impressum')
def impressum():
    try:
        return render_template(
            'impressum.html',
            **page_meta(
                title='Impressum - PACEr',
                description='Impressum und Kontaktangaben fuer PACEr.',
                canonical_path='/impressum',
            ),
        )

    except Exception as e:
        return 'Error: ' + str(e)


@bp_home.route('/projektInfo')
def projektInfo():
    try:
        record_referral_event('landing_view')
        return render_template(
            'projektInfo.html',
            structured_data=webapp_schema(request.url_root),
            **page_meta(
                title='PACEr - Fahrsport Marathon Zeitrechner',
                description='Berechne Bestzeit, erlaubte Zeit, Hoechstzeit und Kilometer-Splits fuer den Fahrsport-Marathon direkt am Handy.',
                canonical_path='/',
            ),
        )

    except Exception as e:
        return 'Error: ' + str(e)


@bp_home.route('/robots.txt')
def robots_txt():
    sitemap_url = url_for('home.sitemap_xml', _external=True)
    content = '\n'.join([
        'User-agent: *',
        'Disallow: /admin',
        'Disallow: /adminLogin',
        'Disallow: /adminTools',
        'Disallow: /changePassword',
        'Disallow: /viewReports',
        f'Sitemap: {sitemap_url}',
        '',
    ])
    return Response(content, mimetype='text/plain')


@bp_home.route('/sw.js')
def service_worker():
    sw_path = os.path.join(current_app.static_folder, 'sw.js')
    with open(sw_path, encoding='utf-8') as sw_file:
        content = sw_file.read()
    response = Response(content, mimetype='application/javascript')
    response.headers['Service-Worker-Allowed'] = '/'
    response.headers['Cache-Control'] = 'no-cache'
    return response


@bp_home.route('/sitemap.xml')
def sitemap_xml():
    public_urls = [
        url_for('home.index', _external=True),
        url_for('calculator.rechner', _external=True),
        url_for('tournament.turniere', _external=True),
        url_for('home.aboutUs', _external=True),
        url_for('home.impressum', _external=True),
        url_for('report.report_problem', _external=True),
    ]

    tournaments = Tournament.query.filter_by(is_active=True).order_by(Tournament.datum.desc()).all()
    for tournament in tournaments:
        public_urls.append(url_for('tournament.turnier_detail', tournament_id=tournament.id, _external=True))

    today = date.today().isoformat()
    items = '\n'.join(
        f'  <url><loc>{url}</loc><lastmod>{today}</lastmod></url>'
        for url in public_urls
    )
    content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{items}\n'
        '</urlset>\n'
    )
    return Response(content, mimetype='application/xml')
