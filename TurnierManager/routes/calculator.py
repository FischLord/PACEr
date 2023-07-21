from flask import Blueprint, render_template, request
from helper import pace, calculatePace, writeStatistics

bp_calculator = Blueprint('calculator', __name__)

@bp_calculator.route('/pacer', methods=['GET', 'POST'])
def pacer():
    if request.method == 'POST':
        try:
            result = None
            laenge = request.form['laenge']
            laenge = int(laenge)
            kmh = request.form['kmh']
            kmh = int(kmh)
            art = request.form['art']
            
            #if laenge:
            bz_sec, hz_sec, ez_sec, bz_min, hz_min, ez_min = calculatePace(laenge, kmh, art)
            ez_result = pace(laenge, ez_min, ez_sec)
            hz_result = pace(laenge, hz_min, hz_sec)
            if bz_min is not None and bz_sec is not None:
                bz_result = pace(laenge, bz_min, bz_sec)
            else:
                bz_result = None
            writeStatistics()
            return render_template('pacer/pacer.html', laenge=laenge, kmh=kmh, art=art, bz_result=bz_result, ez_result=ez_result, hz_result=hz_result)
            #else:
            #    return render_template('pacer.html', laenge=laenge, kmh=kmh, art=art, bz_sec=bz_sec, hz_sec=hz_sec, ez_sec=ez_sec, bz_min=bz_min, hz_min=hz_min, ez_min=ez_min, result=None)

        except Exception as e:
            return 'Error: ' + str(e)
    else:
        return render_template('pacer/pacer.html', laenge=None, kmh=None, art=None, bz_sec=None, hz_sec=None, ez_sec=None, bz_min=None, hz_min=None, ez_min=None, result=None)

# not implemented:
# feature that you can calculate only with one type of pace
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

            #if laenge is not None:
            ez_result = pace(laenge, ez_min, ez_sec)
            hz_result = pace(laenge, hz_min, hz_sec)
            if bz_min is not None and bz_sec is not None:
                bz_result = pace(laenge, bz_min, bz_sec)
                result = {"bz": bz_result, "hz": hz_result, "ez": ez_result}
            writeStatistics()
            return render_template('pacer/pacerOld.html', laenge=laenge, bz_sec=bz_sec, hz_sec=hz_sec, ez_sec=ez_sec, bz_min=bz_min, hz_min=hz_min, ez_min=ez_min, bz_result=bz_result, ez_result=ez_result, hz_result=hz_result)
            #else:
            #    return render_template('pacerOld.html', laenge=laenge, bz_sec=bz_sec, hz_sec=hz_sec, ez_sec=ez_sec, bz_min=bz_min, hz_min=hz_min, ez_min=ez_min, result=None)

        except Exception as e:
            return 'Error: ' + str(e)
    else:
        return render_template('pacer/pacerOld.html', laenge=None, bz_sec=None, hz_sec=None, ez_sec=None, bz_min=None, hz_min=None, ez_min=None, result=None)