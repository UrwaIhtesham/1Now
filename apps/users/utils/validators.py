import re
from django.core.exceptions import ValidationError

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'                                                       #email regex to va;idate email correct: abc@gmail.com etc
PASSWORD_REGEX = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()_+=\-{}[\]|:;"<>,.?/~`]).{6,}$'       #password regex to validate correct: abc123#@$ etc
SQL_CHARS = ["'", '"', ";", "--", "/", "*/"]                                                    # not including sql symbols to avoid sql injections

#helper function to validate email
def validate_email(email):
    if not re.match(EMAIL_REGEX, email):
        raise ValidationError("Invalid email format.")
    return email

#helper function to validate password
def validate_password(password):
    #checks for sql symbols
    if any(char in password for char in SQL_CHARS):
        raise ValidationError("Password contains unsafe characters.")
    #checks for correct password syntax
    if not re.match(PASSWORD_REGEX, password):
        raise ValidationError(
            "Password must be atleast 6 characters long including number, letter and special character(!@#$%^&:<>?)."
        )
    return password