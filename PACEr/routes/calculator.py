from flask import Blueprint, render_template, request
from helper import pace, calculatePace

bp_calculator = Blueprint('calculator', __name__)

@bp_calculator.route('/pacer', methods=['GET', 'POST'])
def pacer():
    if request.method == 'POST':
        try:
            laenge = request.form['laenge']
            laenge = int(laenge)
            kmh = request.form['kmh']
            kmh = int(kmh)
            art = request.form['art']

            if laenge is not None:
                bz_sec, hz_sec, ez_sec, bz_min, hz_min, ez_min = calculatePace(laenge, kmh, art)
                result = pace(laenge, bz_sec, hz_sec, ez_sec, bz_min, hz_min, ez_min)
                return render_template('pacer.html', laenge=laenge, kmh=kmh, art=art, bz_sec=bz_sec, hz_sec=hz_sec, ez_sec=ez_sec, bz_min=bz_min, hz_min=hz_min, ez_min=ez_min, result=result)

            else:
                return render_template('pacer.html', laenge=laenge, kmh=kmh, art=art, bz_sec=bz_sec, hz_sec=hz_sec, ez_sec=ez_sec, bz_min=bz_min, hz_min=hz_min, ez_min=ez_min, result=None)

        except Exception as e:
            return 'Error: ' + str(e)
    else:
        return render_template('pacer.html', laenge=None, kmh=None, art=None, bz_sec=None, hz_sec=None, ez_sec=None, bz_min=None, hz_min=None, ez_min=None, result=None)

@bp_calculator.route('/pacerOld', methods=['GET', 'POST'])
def pacerOld():
    if request.method == 'POST':
        try:
            laenge = request.form['laenge']
            laenge = int(laenge)
            bz_sec = request.form['bz_sec']
            hz_sec = request.form['hz_sec']
            ez_sec = request.form['ez_sec']
            bz_min = request.form['bz_min']
            hz_min = request.form['hz_min']
            ez_min = request.form['ez_min']

            if laenge is not None:
                result = pace(laenge, bz_sec, hz_sec, ez_sec, bz_min, hz_min, ez_min)
                return render_template('pacerOld.html', laenge=laenge, bz_sec=bz_sec, hz_sec=hz_sec, ez_sec=ez_sec, bz_min=bz_min, hz_min=hz_min, ez_min=ez_min, result=result)

            else:
                return render_template('pacerOld.html', laenge=laenge, bz_sec=bz_sec, hz_sec=hz_sec, ez_sec=ez_sec, bz_min=bz_min, hz_min=hz_min, ez_min=ez_min, result=None)

        except Exception as e:
            return 'Error: ' + str(e)
    else:
        return render_template('pacerOld.html', laenge=None, bz_sec=None, hz_sec=None, ez_sec=None, bz_min=None, hz_min=None, ez_min=None, result=None)