import re
from django.core.exceptions import ValidationError
from apps.users.models.booking import Booking

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
    
'''
FOR BOOKING FIELDS
'''

#helper function to validate start date and enddate
def validate_dates(start_date, end_date):
    if start_date > end_date:
        raise ValidationError("Start date must be before end date.")

#helper function to validate booking overlaps 
def validate_overlap(vehicle, start_date, end_date):
    overlaps = Booking.objects.filter(
        vehicle=vehicle,
        start_date__lte=end_date,
        end_date__gte=start_date
    ).exists()

    if overlaps:
        raise ValidationError("This vehicle is already booked for the selected dates.")
    
'''
BONUS TASKS VALIDATORS
'''