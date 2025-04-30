from flask import Blueprint, render_template, request
from helper import pace, calculatePace, writeStatistics

bp_calculator = Blueprint('calculator', __name__)

# Maximal erlaubte Streckenlänge in Metern, um Server-Überlastung zu vermeiden
MAX_LENGTH = 100000  # z.B. 100 km

@bp_calculator.route('/pacer', methods=['GET', 'POST'])
def pacer():
    if request.method == 'POST':
        try:
            laenge = int(request.form['laenge'])
            # Validierung der Streckenlänge
            if laenge <= 0 or laenge > MAX_LENGTH:
                notification = f"Bitte geben Sie eine Streckenlänge zwischen 1 und {MAX_LENGTH} Metern ein."
                return render_template(
                    'pacer.html',
                    laenge=None,
                    kmh=None,
                    art=None,
                    notification=notification,
                    notificationName='Fehler'
                )

            kmh = int(request.form['kmh'])
            art = request.form['art']

            # Berechnung
            bz_sec, hz_sec, ez_sec, bz_min, hz_min, ez_min = calculatePace(laenge, kmh, art)
            ez_result = pace(laenge, ez_min, ez_sec)
            hz_result = pace(laenge, hz_min, hz_sec)
            bz_result = pace(laenge, bz_min, bz_sec) if bz_min is not None else None

            writeStatistics()
            return render_template(
                'pacer.html',
                laenge=laenge,
                kmh=kmh,
                art=art,
                bz_result=bz_result,
                ez_result=ez_result,
                hz_result=hz_result
            )
        except Exception as e:
            return 'Error: ' + str(e)
    else:
        return render_template(
            'pacer.html',
            laenge=None,
            kmh=None,
            art=None,
            bz_sec=None,
            hz_sec=None,
            ez_sec=None,
            bz_min=None,
            hz_min=None,
            ez_min=None,
            result=None
        )

@bp_calculator.route('/pacerOld', methods=['GET', 'POST'])
def pacerOld():
    if request.method == 'POST':
        try:
            laenge = int(request.form['laenge'])
            # Validierung der Streckenlänge
            if laenge <= 0 or laenge > MAX_LENGTH:
                notification = f"Bitte geben Sie eine Streckenlänge zwischen 1 und {MAX_LENGTH} Metern ein."
                return render_template(
                    'pacerOld.html',
                    laenge=None,
                    notification=notification,
                    notificationName='Fehler'
                )

            # Eingabezeiten
            bz_min = int(request.form['bz_min'])
            bz_sec = int(request.form['bz_sec'])
            ez_min = int(request.form['ez_min'])
            ez_sec = int(request.form['ez_sec'])
            hz_min = int(request.form['hz_min'])
            hz_sec = int(request.form['hz_sec'])

            # Berechnung
            ez_result = pace(laenge, ez_min, ez_sec)
            hz_result = pace(laenge, hz_min, hz_sec)
            bz_result = pace(laenge, bz_min, bz_sec)

            writeStatistics()
            return render_template(
                'pacerOld.html',
                laenge=laenge,
                bz_result=bz_result,
                ez_result=ez_result,
                hz_result=hz_result
            )
        except Exception as e:
            return 'Error: ' + str(e)
    else:
        return render_template(
            'pacerOld.html',
            laenge=None,
            bz_sec=None,
            hz_sec=None,
            ez_sec=None,
            bz_min=None,
            hz_min=None,
            ez_min=None,
            result=None
        )
