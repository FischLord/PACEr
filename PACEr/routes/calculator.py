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

            if laenge is not None:
                calculatePace()
                result = pace(laenge, bz_sec, hz_sec, ez_sec, bz_min, hz_min, ez_min)
                return render_template('pacer.html', laenge=laenge, kmh=kmh, bz_sec=bz_sec, hz_sec=hz_sec, ez_sec=ez_sec, bz_min=bz_min, hz_min=hz_min, ez_min=ez_min, result=result)

            else:
                return render_template('pacer.html', laenge=laenge, kmh=kmh, bz_sec=bz_sec, hz_sec=hz_sec, ez_sec=ez_sec, bz_min=bz_min, hz_min=hz_min, ez_min=ez_min, result=None)

        except Exception as e:
            return 'Error: ' + str(e)
    else:
        return render_template('pacer.html', laenge=None, bz_sec=None, hz_sec=None, ez_sec=None, bz_min=None, hz_min=None, ez_min=None, result=None)
