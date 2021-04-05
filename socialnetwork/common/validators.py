import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def user_name_validator(user_name):
    regex = "(\+98|0)?9\d{9}"
    phone_number_match = re.match(regex, user_name)
    if not phone_number_match:
        if user_name.find("@") != -1:
            try:
                validate_email(user_name)
            except validate_email.ValidationError:
                raise user_name('Invalid Email')
        else:
            raise ValidationError('Invalid phone number')


def name_validation(name):
    import re

    english_check = re.compile(r'[a-zA-Z]+')
    if english_check.match(name):
        pass
    else:
        raise ValidationError('Invalid phone number')
