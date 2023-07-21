from flask import Blueprint, render_template, request
from random import randint
from datetime import date
from helper import getDirPath
import os
import json
bp_report = Blueprint('report', __name__)


@bp_report.route('/reportProblem', methods=['GET', 'POST'])
def reportProblem():
    if request.method == 'POST':
        try:
            # create folder reports/date
            currentDate = date.today().strftime("%d.%m.%Y")
            absPath = getDirPath()
            folderPath = absPath + '/reports/' + currentDate
            # when more then 100 issues get reported in one day, stop accepting reports
            if not os.path.exists(folderPath):
                os.makedirs(folderPath)
            if len(os.listdir(folderPath)) <= 100:
                name = request.form['name']
                vorname = request.form['vorname']
                email = request.form['email']
                issue = request.form['issue']
                # write in json file and save in folder reports/date/name + random nuimber.json
                filename = name + vorname + str(randint(0, 1000)) + '.json'
                filepath = folderPath + '/' + filename
                report = open(filepath, 'w')
                report_dict = {'Name': name, 'Vorname': vorname, 'Email': email, 'Issue': issue}
                json.dump(report_dict, report)
                report.close()
                return render_template('projektInfo.html', notification='Ihr Problem wurde erfolgreich gemeldet.', notificationName='Info')
            else:
                return render_template('reportProblem.html', notification='Heute wurden bereits 100 Probleme gemeldet. Um eine Überlastung zu vermeiden, können heute keine weiteren Probleme gemeldet werden. Bitte versuchen Sie es morgen erneut.', notificationName='Warnung' , name=name, vorname=vorname, email=email, issue=issue)
        except Exception as e:
            return 'Error: ' + str(e)
    else:
        try:
            return render_template('reportProblem.html')
        except Exception as e:
            return 'Error: ' + str(e)