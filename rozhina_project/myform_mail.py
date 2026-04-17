import re

def check_email(email):
    pattern = r'^[A-Za-z0-9]([-._]?[A-Za-z0-9]){2,31}@[A-Za-z0-9]([-.]?[A-Za-z0-9]){1,39}\.[A-Za-z]{2,7}$'
    return re.match(pattern, email) is not None