import os
import re
from django.contrib import messages

def emailValidate(request,key):
    if not key or key.strip() == '':
        messages.error(request,"Email cannot be blank")
        return False
    elif not key.strip().endswith('@skit.ac.in'):
        messages.error(request, 'Mail should always end with @skit.ac.in')
        return False
    else:
        return True


def mobileNumberValidate(request,key):
    mobilepattern = r'[6789][0-9]{9}'
    if not key or key == '':
        error_message = f"Mobile Number cannot be empty"
        messages.error(request, error_message)
        return False
    elif not re.match(mobilepattern,key):
        error_message = f"Mobile Number cannot contains special characters,digits,tabs or newline."
        messages.error(request, error_message)
        return False
    else:
        return True

def validate_pan(pan_number):
    # The Regex Pattern
    # [A-Z]{3} -> First 3 alphabets
    # [PCHFATBLJG] -> 4th character (Status)
    # [A-Z] -> 5th character (Surname initial)
    # [0-9]{4} -> Next 4 digits
    # [A-Z] -> Last alphabet
    pattern = r'^[A-Z]{3}[PCHFATBLJG][A-Z][0-9]{4}[A-Z]$'

    # Ensure the input is treated as uppercase and stripped of whitespace
    pan_number = str(pan_number).upper()

    if re.match(pattern, pan_number):
        return True
    else:
        return False

def nameValidate(request,key,tag):
    if not key or key == '':
        error_message = f"{tag} cannot be empty"
        messages.error(request,error_message)
        return False
    else:
        return True

def alphanumnameValidate(request,key,tag):
    namepattern = re.compile(r'[^a-zA-Z0-9 ]')
    if not key or key == '':
        error_message = f"{tag} cannot be empty"
        messages.error(request, error_message)
        return False
    elif namepattern.search(key):
        error_message = f"{tag} cannot contains special characters,digits,tabs or newline."
        messages.error(request, error_message)
        return False
    else:
        return True

def numberValidate(request,key,tag):
    if not key:
        error_message = f"{tag} cannot be empty"
        messages.error(request,error_message)
        return False
    else:
        return True

def radiocheck(request,key,tag):
    if len(key) < 1:
        error_message = f"Please select at least one {tag}"
        messages.error(request, error_message)
        return False
    else:
        return True

def fileValidate(request,key,tag):

    limit_mb = 2
    if key.size > limit_mb * 1024 * 1024:
        messages.error(request, f"{tag} exceeded the file upload limit(10mb)")
        return False

    allowed_extension = ['.pdf']
    extenstion = os.path.splitext(key.name)[1].lower()

    if extenstion not in allowed_extension:
        messages.error(request, f"{tag} should be of .pdf format")
        return False

    allowed_mime_types = ['application/pdf']
    if key.content_type not in allowed_mime_types:
        messages.error(request, f"{tag} should be of content type pdf")
        return False

    return True

def addressValidate(request,key,tag):
    pattern = re.compile(r'[^a-zA-Z0-9\s,./-]')
    if not key or key == '':
        error_message = f"{tag} cannot be empty"
        messages.error(request, error_message)
        return False
    elif pattern.search(key):
        result = pattern.search(key)
        error_message = f"{tag} cannot contain {result.group()}"
        messages.error(request, error_message)
        return False
    else:
        return True

def imageFileValidate(request,key,tag):

    limit_mb = 2
    if key.size > limit_mb * 1024 * 1024:
        messages.error(request, f"{tag} exceeded the file upload limit(10mb)")
        return False

    allowed_extension = ['.jpg','.jpeg','.png']
    extenstion = os.path.splitext(key.name)[1].lower()

    if extenstion not in allowed_extension:
        messages.error(request, f"{tag} should be of .pdf format")
        return False

    allowed_mime_types = ['image/jpeg','image/png']
    if key.content_type not in allowed_mime_types:
        messages.error(request, f"{tag} should be of content type pdf")
        return False

    return True