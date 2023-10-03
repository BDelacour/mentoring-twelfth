from getpass import getpass
from typing import List, Dict

from python_p12.models.user import User
from python_p12.validators import check_password, ValidationException, ValidationError, check_email, check_name


def _get_valid_fullname() -> str:
    error_type_message: Dict[ValidationError] = {
        ValidationError.NAME_TOO_SHORT: 'This name is too short (min 3 char.).',
    }

    for _ in range(3):
        try:
            fullname = input('Enter Fullname : ')
            check_name(fullname)
            return fullname
        except ValidationException as e:
            print(error_type_message[e.error_type])
    raise ValidationException(ValidationError.FAILED)


def _get_valid_email() -> str:
    error_type_message: Dict[ValidationError] = {
        ValidationError.EMAIL_INVALID: 'This is not a valid email address.',
    }

    for _ in range(3):
        try:
            email = input('Enter Email : ')
            check_email(email)
            return email
        except ValidationException as e:
            print(error_type_message[e.error_type])
    raise ValidationException(ValidationError.FAILED)


def _get_valid_password() -> str:
    error_type_message: Dict[ValidationError] = {
        ValidationError.PASSWORD_TOO_SHORT: 'Your password is too short.',
        ValidationError.PASSWORD_MISSING_LOWERCASE: 'Your password misses a lowercase character.',
        ValidationError.PASSWORD_MISSING_UPPERCASE: 'Your password misses an uppercase character.',
        ValidationError.PASSWORD_MISSING_SYMBOL: 'Your password misses a symbol.',
    }

    for _ in range(3):
        try:
            password = getpass('Enter Password (min 12 characters, 1 lowercase, 1 uppercase, 1 digit, 1 symbol) : ')
            check_password(password)
            return password
        except ValidationException as e:
            print(error_type_message[e.error_type])
    raise ValidationException(ValidationError.FAILED)


def display_user_form():
    fullname = _get_valid_fullname()
    email = _get_valid_email()
    password = _get_valid_password()

    return {
        'fullname': fullname,
        'email': email,
        'password': password
    }


def display_user(user: User, separator: bool = False):
    if separator:
        print("---")
    print(f"Id : {user.id}\nFullname : {user.fullname}\nEmail : {user.email}")


def display_users(user_list: List[User]):
    for i, user in enumerate(user_list):
        display_user(user, separator=i > 0)


def display_user_select(user_list: List[User]):
    user_select = {str(i + 1): user for i, user in enumerate(user_list)}
    for row, user in user_select.items():
        print(f"{row} => {user.email} [uid={user.id}]")
    for _ in range(3):
        selected_user = input(f"Select an user (1-{len(user_list)}) : ")
        if selected_user in user_select:
            return user_select[selected_user]
    raise ValidationException(ValidationError.FAILED)


def display_user_deletion(user: User):
    print(f"User \"{user.email}\" [uid={user.id}] successfully deleted")
