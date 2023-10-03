import click
from sqlalchemy import select
from sqlalchemy.orm import Session

from python_p12.database import orm
from python_p12.models.user import User
from python_p12.views.users import display_users, display_user_form, display_user


@click.group(name='users')
def users():
    pass


@users.command(name='create')
@orm
def _create(session: Session):
    user_info = display_user_form()
    user = User(
        fullname=user_info['fullname'],
        email=user_info['email'],
    )
    user.set_password(user_info['password'])
    session.add(user)
    return display_user(user)


@users.command(name='list')
@orm
def _list(session):
    user_list = session.scalars(select(User))
    return display_users(user_list)
