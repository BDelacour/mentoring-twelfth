from getpass import getpass
from typing import List

from python_p12.models.user import User


def display_user_form():
    fullname = input('Enter Fullname : ')
    email = input('Enter Email : ')
    password = getpass('Enter Password : ')
    return {
        'fullname': fullname,
        'email': email,
        'password': password
    }


def display_user(user: User):
    print(f"Id : {user.id}\nFullname : {user.fullname}\nEmail : {user.email}")


def display_users(user_list: List[User]):
    for i, user in enumerate(user_list):
        if i > 0:
            print('---')
        display_user(user)
