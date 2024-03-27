import re

from django.core.exceptions import ObjectDoesNotExist


def password_validator(password):
    if re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,25}$', password):
        return True
    return False


def expire_token(user):
    try:
        user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass
