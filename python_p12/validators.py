import re
from enum import Enum


class ValidationError(Enum):
    FAILED = 0
    PASSWORD_TOO_SHORT = 1
    PASSWORD_MISSING_DIGIT = 2
    PASSWORD_MISSING_LOWERCASE = 3
    PASSWORD_MISSING_UPPERCASE = 4
    PASSWORD_MISSING_SYMBOL = 5
    EMAIL_INVALID = 6
    NAME_TOO_SHORT = 7


class ValidationException(Exception):
    error_type: ValidationError

    def __init__(self, error_type: ValidationError, *args: object) -> None:
        super().__init__(*args)
        self.error_type = error_type


def check_password(passwd):
    if len(passwd) < 12:
        raise ValidationException(ValidationError.PASSWORD_TOO_SHORT)
    if not any(char.isdigit() for char in passwd):
        raise ValidationException(ValidationError.PASSWORD_MISSING_DIGIT)
    if not any(char.islower() for char in passwd):
        raise ValidationException(ValidationError.PASSWORD_MISSING_LOWERCASE)
    if not any(char.isupper() for char in passwd):
        raise ValidationException(ValidationError.PASSWORD_MISSING_UPPERCASE)
    if passwd.isalnum():
        raise ValidationException(ValidationError.PASSWORD_MISSING_SYMBOL)
    return True


def check_email(email):
    regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
    if not regex.fullmatch(email):
        raise ValidationException(ValidationError.EMAIL_INVALID)
    return True


def check_name(name):
    if len(name) < 3:
        raise ValidationException(ValidationError.NAME_TOO_SHORT)
    return True
