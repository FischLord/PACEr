from flask import Blueprint, render_template, request
from helper import *
import os
import json
bp_admin = Blueprint('admin', __name__)


@bp_admin.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    if request.method == 'POST':
        try:
            if request.form['password'] == 'Potsdam1':
                return render_template('admin/adminTools.html', key=True)
            else:
                return render_template('admin/adminLogin.html', notification='Falsches Passwort', notificationName='Warnung', password=request.form['password'])
        except Exception as e:
            return 'Error: ' + str(e)
    else:
        try:
            return render_template('admin/adminLogin.html')
        except Exception as e:
            return 'Error: ' + str(e)
        
@bp_admin.route('/adminTools', methods=['GET', 'POST'])
def adminTools():
    try:
        if request.form['key']:
            return render_template('admin/adminTools.html', key=True)
        else:
            return render_template('admin/adminLogin.html', notification='Falsches Passwort', notificationName='Warnung', password=request.form['password'])
    except Exception as e:
        return 'Error: ' + str(e)
    
    
#################### Reports Section Start ####################
@bp_admin.route('/viewReports', methods=['GET', 'POST'])
def viewReports():
    try:
        # get all reports
        absPath = getDirPath()
        reportsPath = absPath + '/reports'
        reports = []
        for date in sorted(os.listdir(reportsPath), reverse=True):
            for report in sorted(os.listdir(reportsPath + '/' + date)):
                reports.append({
                    'path': reportsPath + '/' + date + '/' + report,
                    'date': date,
                    'name': report
                })
        return render_template('admin/reports/viewReports.html', reports=reports)
    except Exception as e:
        return 'Error: ' + str(e)
    
@bp_admin.route('/displayReport', methods=['GET', 'POST'])
def displayReport():
    # get request for a specific report will be in the form of /displayReport?report=reportPath
    try:
        report = returnReport(reportPath=request.args.get('report'))
        return render_template('admin/reports/displayReport.html', report=report)
    except Exception as e:
        return 'Error: ' + str(e)

#################### Reports Section End ####################

#################### Question Section Start ####################

@bp_admin.route('/viewQuestions', methods=['GET', 'POST'])
def viewQuestions():
    try:
        return render_template('admin/questions/viewQuestions.html')
    except Exception as e:
        return 'Error: ' + str(e)
    
@bp_admin.route('/loadQuestion', methods=['GET', 'POST'])
def loadQuestion():
    return
    
@bp_admin.route('/saveQuestion', methods=['GET', 'POST'])
def saveQuestion():
    return

@bp_admin.route('/deleteQuestion', methods=['GET', 'POST'])
def deleteQuestion():
    return

@bp_admin.route('/editQuestion', methods=['GET', 'POST'])
def editQuestion():
    return

@bp_admin.route('/addQuestion', methods=['GET', 'POST'])
def addQuestion():
    return

#################### Question Section End ####################