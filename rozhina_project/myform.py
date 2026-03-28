from bottle import post, request
from datetime import date
import re
import pdb
import json
with open(r'static\questions.json', 'r') as questions_data:
    questions = json.load(questions_data)
@post('/home', method='post')
def my_form():
    pattern_email = r'^[A-Za-z0-9]([-._]?[A-Za-z0-9]){2,31}@[A-Za-z0-9]([-.]?[A-Za-z0-9]){1,39}\.[A-Za-z]{2,7}$'
    pattern_name = r'^[A-Za-z0-9]{3,100}$'
    pattern_question = r'^[^А-Яа-яЁё]*[A-Za-z][^А-Яа-яЁё]*$'
    mail = request.forms.getunicode('ADRESS').strip().lower()
    question = request.forms.getunicode('QUEST').strip().lower()
    name = request.forms.getunicode('USERNAME').strip()
    i = 0
    if not re.match(pattern_email, mail):
        return "Error: Invalid email format"
    if not re.match(pattern_name, name) or name == "" or name.isdigit():
        return "Error: Invalid username format"
    
    if not re.match(pattern_question, question):
        return "Error: Invalid question format"

    words = question.split(" ")
    while i < len(words):
        if words[i] == '':
            words.remove(words[i])
            continue
        i = i + 1
    question = " ".join(words)
    today = date.today().strftime("%Y-%m-%d")
    already_question = True
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
        already_question = False
        questions.append(new_entry)
    with open(r'static\questions.json', 'w') as questions_data:
        json.dump(questions, questions_data, indent=4)
    if already_question:
         return "This question has already been asked, %s. Please wait for a response" % (name)
    return "Thanks, %s! The answer will be sent to the mail %s. Access Date: %s" % (name, mail, today)