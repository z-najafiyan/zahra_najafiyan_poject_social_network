from django.core.exceptions import ValidationError



def password_validator(password):
    if len(password) != 8:
        raise ValidationError('Please follow the mentioned format:invalid length\n'
                              'The password must be 8 characters long')

