from getpass import getpass
from typing import List

import click

from epic_events.models.role import Roles
from epic_events.models.user import User
from epic_events.validators import validate_name, validate_email, validate_password, validate_role


def display_user(user: User, separator: bool = False):
    if separator:
        print("---")
    print(f"Id : {user.id}\n"
          f"Fullname : {user.fullname}\n"
          f"Email : {user.email}\n"
          f"Role : {user.role.name.capitalize()}")


def display_users(user_list: List[User]):
    for i, user in enumerate(user_list):
        display_user(user, separator=i > 0)


def display_user_exists(user: User):
    raise click.ClickException(f"User \"{user.email}\" already exists")


def display_role_not_exists():
    raise click.ClickException(f"Requested role is not valid ({', '.join([r.name.capitalize() for r in Roles])})")


def display_user_not_exists():
    raise click.ClickException('Requested user is not valid')


def display_user_deletion(user: User):
    print(f"User \"{user.email}\" [uid={user.id}] successfully deleted")


def ask_for_user_update(user: User):
    print("Will modify the following user")
    display_user(user)
    print("---\nLeave empty for same")

    fullname = input("Full name : ") or None
    if fullname:
        validate_name(None, "fullname", fullname)

    email = input("Email : ") or None
    if email:
        validate_email(None, "email", email)

    role = input("Role : ") or None
    if role:
        validate_role(None, "role", role)

    password = getpass("New password : ") or None
    if password:
        validate_password(None, None, password)
        old_password = getpass("Old password : ")
        if not user.check_password(old_password):
            raise click.ClickException("Password mismatch")

    return {
        'fullname': fullname,
        'email': email,
        'password': password
    }
