from bottle import post, request
from datetime import date
import re

@post('/home', method='post')
def my_form():
    pattern = r'^[A-Za-z0-9]([-._]?[A-Za-z0-9]){2,31}@[A-Za-z0-9]([-.]?[A-Za-z0-9]){1,39}\.[A-Za-z]{2,7}$'
    mail = request.forms.get('ADRESS').strip()
    name = request.forms.get('USERNAME')
    today = date.today().strftime("%Y-%m-%d")
    if not re.match(pattern, mail):
        return "Error: Invalid email format"
    if (name.isspace()):
        return "Error: Uncorrect username (contains only spaces)"
    if (request.forms.get('QUEST').isspace()):
        return "Error: Uncorrect question (contains only spaces)"
    return "Thanks, %s! The answer will be sent to the mail %s. Access Date: %s" % (name, mail, today)