from bottle import post, request
import re

@post('/home', method='post')
def my_form():
    pattern = r'^[A-Za-z0-9]([A-Za-z0-9._-]{0,62}[A-Za-z0-9])?@[A-Za-z0-9]+([-.][A-Za-z0-9]+)*\.[A-Za-z]{2,}$'
    mail = request.forms.get('ADRESS')
    if not re.match(pattern, mail):
        return "Error: Invalid email format"
    return "Thanks! The answer will be sent to the mail %s" % mail