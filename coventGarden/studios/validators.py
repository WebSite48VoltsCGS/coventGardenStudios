import re
from django.core.exceptions import ValidationError

"""
Constants
"""
MIN_LENGTH = 8
MIN_NUMBER = 1
MIN_UPPER = 1
MIN_SPECIAL = 1



"""
Error messages
    - error_messages_password
    - error_messages_phone
"""
error_messages_password = {
    "password_length": "Votre mot de passe ne contient pas %i caractères." % MIN_LENGTH,
    "password_number": "Votre mot de passe ne contient pas de chiffre.",
    "password_upper": "Votre mot de passe ne contient pas de majuscule.",
    "password_special": "Votre mot de passe ne contient pas de caractère spécial.",
}

error_messages_phone = {
    "phone_invalid": "Le numéro de téléphone saisi n'est pas valide."
}



"""
Help text
    - help_text_password
"""
help_text_password = [
    "Votre mot de passe doit contenir au moins %i caractères." % MIN_LENGTH,
    "Votre mot de passe doit contenir au moins %i chiffre." % MIN_NUMBER,
    "Votre mot de passe doit contenir au moins %i majuscule." % MIN_UPPER,
    "Votre mot de passe doit contenir au moins %i caractère spécial." % MIN_SPECIAL,
]



"""
CustomPasswordValidator
    - length_validator
    - number_validator
    - upper_validator
    - special_validator
"""
def length_validator(password):
    """
    A validator that uses Regex to check that the password entered contains at least MIN_LENGTH characters
    """
    if len(password) < MIN_LENGTH:
        raise ValidationError(error_messages_password["password_length"], code='password_length', params={'min_length': MIN_LENGTH})

def number_validator(password):
    """
    A validator that uses Regex to check that the password entered contains a number
    """
    if not re.findall('\d', password):
        raise ValidationError(error_messages_password["password_number"], code='password_number')

def upper_validator(password):
    """
    A validator that uses Regex to check that the password entered contains a uppercase letter
    """
    if not re.findall('[A-Z]', password):
        raise ValidationError(error_messages_password["password_upper"], code='password_upper')

def special_validator(password):
    """
    A validator that uses Regex to check that the password entered contains a special character
    """
    if not re.findall('[@#$%!^&*]', password):
        raise ValidationError(error_messages_password["password_special"], code='password_special')



"""
Phone validator
    - phone_validator
"""
def phone_validator(value):
    """
    A validator that uses Regex to check that the value entered meets multiple conditions
    """
    phone_regex = r'^0[1-7]\d{8}$'  # Regex pour vérifier les conditions
    if not re.match(phone_regex, value):
        raise ValidationError(error_messages_phone["phone_invalid"], code='phone_invalid')



"""
Validators
"""
CustomPasswordValidator = [length_validator, number_validator, upper_validator, special_validator]
CustomPhoneValidator = [phone_validator]
