from getpass import getpass
from typing import List

import click

from epic_events.models.user import User
from epic_events.validators import validate_name, validate_email, validate_password


def display_user(user: User, separator: bool = False):
    if separator:
        print("---")
    print(f"Id : {user.id}\nFullname : {user.fullname}\nEmail : {user.email}")


def display_users(user_list: List[User]):
    for i, user in enumerate(user_list):
        display_user(user, separator=i > 0)


def display_user_exists(user: User):
    raise click.ClickException(f"User \"{user.email}\" already exists")


def display_user_not_exists():
    raise click.ClickException('Requested user does not exist')


def display_user_deletion(user: User):
    print(f"User \"{user.email}\" [uid={user.id}] successfully deleted")


def ask_for_user_update(user: User):
    print("Will modify the following user")
    display_user(user)
    print("---\nLeave empty for same")

    fullname = input("Full name : ")
    if fullname != "":
        validate_name(None, "fullname", fullname)

    email = input("Email : ")
    if email != "":
        validate_email(None, "email", email)

    password = getpass("New password : ")
    if password != "":
        validate_password(None, None, password)
        old_password = getpass("Old password : ")
        if not user.check_password(old_password):
            raise click.ClickException("Password mismatch")

    return {
        'fullname': fullname,
        'email': email,
        'password': password
    }

