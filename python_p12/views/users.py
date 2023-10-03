from typing import List

import click

from python_p12.models.user import User


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
    raise click.ClickException(f"Requested user does not exist")


def display_user_deletion(user: User):
    print(f"User \"{user.email}\" [uid={user.id}] successfully deleted")
