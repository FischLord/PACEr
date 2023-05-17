from flask import Blueprint, render_template
bp_home = Blueprint('home', __name__)



@bp_home.route('/')
def start():
    try:
        return render_template('index.html')

    except Exception as e:
        return 'Error: ' + str(e)