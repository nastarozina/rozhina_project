from bottle import post, request
from datetime import date
import re
import pdb
import json
with open(r'static\questions.json', 'r') as questions_data:
    questions = json.load(questions_data)
@post('/home', method='post')
def my_form():
    pattern = r'^[A-Za-z0-9]([-._]?[A-Za-z0-9]){2,31}@[A-Za-z0-9]([-.]?[A-Za-z0-9]){1,39}\.[A-Za-z]{2,7}$'
    mail = request.forms.get('ADRESS').strip()
    question = request.forms.get('QUEST').strip()
    name = request.forms.get('USERNAME').strip()
    today = date.today().strftime("%Y-%m-%d")
    already_question = True
    if not re.match(pattern, mail):
        return "Error: Invalid email format"
    if (name.isspace()):
        return "Error: Uncorrect username (contains only spaces)"
    if (question.isspace()):
        return "Error: Uncorrect question (contains only spaces)"
    
    user_entry = next((item for item in questions if item["mail"] == mail), None)

    if user_entry:
        if user_entry["name"] != name:
            user_entry["name"] = name
        if question not in user_entry["questions"]:
            user_entry["questions"].append(question)
            already_question = False
    else:
        new_entry = {
            "mail": mail,
            "name": name,
            "questions": [question]
        }
        questions.append(new_entry)
    with open(r'static\questions.json', 'w') as outfile:
        json.dump(questions, outfile, indent=4)
    if already_question:
         return "This question has already been asked, %s. Please wait for a response" % (name)
    return "Thanks, %s! The answer will be sent to the mail %s. Access Date: %s" % (name, mail, today)