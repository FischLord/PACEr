from flask import Blueprint, render_template, request
bp_report = Blueprint('report', __name__)


@bp_report.route('/reportProblem', methods=['GET', 'POST'])
def reportProblem():
    if request.method == 'POST':
        try:
            return render_template('reportProblem.html')
        except Exception as e:
            return 'Error: ' + str(e)
    else:
        render_template('reportProblem.html')