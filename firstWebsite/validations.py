import datetime
import os
import re

def emailValidate(key):
    if not key or key.strip() == '':
        return False, "Email cannot be blank"
    elif not key.strip().endswith('@skit.ac.in'):
        return False, 'Mail should always end with @skit.ac.in'
    else:
        return True, ''


def mobileNumberValidate(key):
    mobilepattern = r'[6789][0-9]{9}'
    if not key or key == '':
        error_message = f"Mobile Number cannot be empty"
        return False, error_message
    elif not re.match(mobilepattern,key):
        error_message = f"Mobile Number cannot contains special characters,digits,tabs or newline."
        return False, error_message
    else:
        return True, ''

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
        return True, ''
    else:
        return False, 'Please enter a valid PAN Number'

# this is for the validation of the pshd -> Passing Year of Highest Degree
def pshdValidate(key, tag):
    if key is None or key == "":
        error_message = f"{tag} cannot be empty"
        return False, error_message

    current_year = datetime.now().year

    if int(key) > current_year:
        error_message = f"{tag} cannot be greater than {current_year}"
        return False, error_message

    return True, ''

def nameValidate(key,tag):
    if not key or key == '':
        error_message = f"{tag} cannot be empty"
        return False, error_message
    else:
        return True, ''

def alphanumnameValidate(key,tag):
    namepattern = re.compile(r'[^a-zA-Z0-9 ]')
    if not key or key == '':
        error_message = f"{tag} cannot be empty"
        return False, error_message
    elif namepattern.search(key):
        error_message = f"{tag} cannot contains special characters,digits,tabs or newline."
        return False, error_message
    else:
        return True, ''

def numberValidate(key,tag):
    if key is None or key == "":
        error_message = f"{tag} cannot be empty"
        return False, error_message
    else:
        return True, ''

def radiocheck(key,tag):
    if len(key) < 1:
        error_message = f"Please select at least one {tag}"
        return False, error_message
    else:
        return True, ''

def fileValidate(key,tag):
    limit_mb = 2
    if key.size > limit_mb * 1024 * 1024:
        return False, f'{tag} exceeded the file upload limit(2 mb).\nPlease compress the file under 2 MB.\nCompressor link(PDF):- <a href="https://www.ilovepdf.com/compress_pdf" target="_blank">Click Here</a>.\nCompressor link(Image):- <a href="https://squoosh.app/" target="_blank">Click Here</a>.'

    allowed_extension = ['.pdf','.jpg','.jpeg','.png']
    extenstion = os.path.splitext(key.name)[1].lower()

    if extenstion not in allowed_extension:
        return False, f"{tag} should be of .pdf,'.jpg','.jpeg','.png' format"

    allowed_mime_types = ['application/pdf','image/jpeg','image/png']
    if key.content_type not in allowed_mime_types:
        return False, f"{tag} should be of content type pdf, jpg, png"

    return True, ''

def addressValidate(key,tag):
    pattern = re.compile(r'[^a-zA-Z0-9\s,./-]')
    if not key or key == '':
        error_message = f"{tag} cannot be empty"
        return False, error_message
    elif pattern.search(key):
        result = pattern.search(key)
        error_message = f"{tag} cannot contain {result.group()}"
        return False, error_message
    else:
        return True, ''

def imageFileValidate(key,tag):
    limit_mb = 2
    if key.size > limit_mb * 1024 * 1024:
        return False, f'{tag} exceeded the file upload limit(2 mb).\nPlease compress the file under 2 MB.\nCompressor link:- <a href="https://squoosh.app/" target="_blank">Click Here</a>.'

    allowed_extension = ['.jpg','.jpeg','.png']
    extenstion = os.path.splitext(key.name)[1].lower()

    if extenstion not in allowed_extension:
        return False, f"{tag} should be of .png, .jpeg, .jpg format"

    allowed_mime_types = ['image/jpeg','image/png']
    if key.content_type not in allowed_mime_types:
        return False, f"{tag} should be of content type image/jpeg or image/png"

    return True, ''