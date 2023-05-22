from flask import Blueprint, render_template
bp_calculator = Blueprint('calculator', __name__)

@bp_calculator.route('/calculator')
def calculator():
    try:
        return render_template('calculator.html')

    except Exception as e:
        return 'Error: ' + str(e)