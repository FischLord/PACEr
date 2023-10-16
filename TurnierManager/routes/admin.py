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
        absPath = getDirPath()
        folderPath = absPath + '/questions/'
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        jsonPath = folderPath + 'questions.json'
        # read the json file and get the questions list
        with open(jsonPath, "r") as f:
            json_data = json.load(f)
            questions = json_data["questions"]
        # render the template with the questions list
        return render_template('admin/questions/viewQuestions.html', questions=questions)
    except Exception as e:
        return 'Error: ' + str(e)

    
@bp_admin.route('/loadQuestion/<int:id>', methods=['GET', 'POST'])
def loadQuestion(id):
    print(id)
    # get the id of the question to load
    # id = request.args.get('id')
    # get the path to the json file
    absPath = getDirPath()
    folderPath = absPath + '/questions/'
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    jsonPath = folderPath + 'questions.json'
    # read the json file and get the questions list
    with open(jsonPath, "r") as f:
        json_data = json.load(f)
        questions = json_data["questions"]
    # find the question with the id
    # for question in questions:
    #     if question["id"] == int(id):
    #         # extract the information from the question and render the template with the information
    #         # use a different variable to store the question text
    #         question_text = question["question"]
    #         category = question["category"]
    #         difficulty = question["difficulty"]
    #         type = question["type"]
    #         imagepath = question["image"]
    #         answers = question["answers"]
    #         correct_answers = question["correct_answers"]
    #         explanation = question["explanation"]
    #         official = question["official"]
    #         # load the image from the path and give it to the template
    #         image = open(imagepath, 'rb')
    #         image = image.read()
    #         return render_template('admin/questions/showQuestion.html', id=id, question=question_text, category=category, difficulty=difficulty, type=type, image=image, answers=answers, correct_answers=correct_answers, explanation=explanation, official=official)
        question = questions[id]
        return render_template('admin/questions/showQuestion.html', question=question)



@bp_admin.route('/newQuestion', methods=['GET', 'POST'])
def newQuestion():
    absPath = getDirPath()
    folderPath = absPath + '/questions/'
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    jsonPath = folderPath + 'questions.json'
    
    
    question = request.form.get('question')
    category = request.form.get('category')
    difficulty = request.form.get('difficulty') 
    type = request.form.get('type')
    image = request.files.get('image')
    answers = request.form.getlist('answers[]') 
    correct_answers = request.form.getlist('correct_answers[]') 
    explanation = request.form.get('explanation')
    official = request.form.get('official')
    # save the image in the folder under the subfolder with the id and the name of the image
    imageSavePath = folderPath + 'images/' + image.filename
    image.save(imageSavePath)
    
    # check for the highest id in the json document
    newID = getHighestId(jsonPath)
    # create dictionary with the new question
    newQuestion = {"id": newID, "question": question, "category": category, "difficulty": difficulty, "type": type, "image": imageSavePath, "answers": answers, "correct_answers": correct_answers, "explanation": explanation, "official": official}
    # open the json document where all the questions are stored
    # call the checkAndInitJson function with the path to the json file and assign the result to a variable
    json_data = checkAndInitJson(jsonPath)
    # append the new question to the questions list
    json_data["questions"].append(newQuestion)
    # write the json file
    with open(jsonPath, "w") as f:
        json.dump(json_data, f)
    
    with open(jsonPath, "r") as f:
            question_data = json.load(f)
            questions = question_data["questions"]
        # render the template with the questions list
    return render_template('admin/questions/viewQuestions.html', questions=questions)


@bp_admin.route('/deleteQuestion', methods=['GET', 'POST'])
def deleteQuestion():
    return

@bp_admin.route('/editQuestion', methods=['GET', 'POST'])
def editQuestion():
    return

@bp_admin.route('/addQuestion', methods=['GET', 'POST'])
def addQuestion():
    return render_template('admin/questions/addQuestion.html')

#################### Question Section End ####################