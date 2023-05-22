from flask import Blueprint, render_template
bp_home = Blueprint('home', __name__)



@bp_home.route('/')
def index():
    try:
        return render_template('index.html')

    except Exception as e:
        return 'Error: ' + str(e)
    
@bp_home.route('/aboutUs')
def aboutUs():
    try:
        return render_template('aboutUs.html')

    except Exception as e:
        return 'Error: ' + str(e)
@bp_home.route('/impressum')
def impressum():
    try:
        return render_template('impressum.html')

    except Exception as e:
        return 'Error: ' + str(e)

@bp_home.route('/projektInfo')
def projektInfo():
    try:
        return render_template('projektInfo.html')

    except Exception as e:
        return 'Error: ' + str(e)
    
@bp_home.route('/report')
def report():
    try:
        return render_template('report.html')
    except Exception as e:
        return 'Error: ' + str(e)