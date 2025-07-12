import re
from django.core.exceptions import ValidationError

'''
FOR USER FIELDS
'''

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

'''
FOR VEHICLE FIELDS
'''

PLATE_REGEX = r'^[A-Z]{2,4}-?\d{3,4}$'

#helper function to validate make of the car
def validate_make(make):
    #if no make then raise error
    if not make or make.strip() == "":
        raise ValidationError("Make is required.")
    #make cannot have all the digits
    if make.isdigit():
        raise ValidationError("Make cannot be a number.")
    
#helper function to validate plate number
#plate can always be beytween abc-123 to abcd-1234
def validate_plate(plate):
    if not re.match(PLATE_REGEX, plate, re.IGNORECASE):
        raise ValidationError("Invalid plate format. Example: abc-1234")