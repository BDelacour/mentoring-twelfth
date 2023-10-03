import click
from sqlalchemy import select
from sqlalchemy.orm import Session

from python_p12.database import orm
from python_p12.auth import authenticated
from python_p12.models.user import User
from python_p12.validators import validate_email, validate_password, validate_name
from python_p12.views.users import display_users, display_user, display_user_deletion, display_user_exists, \
    display_user_not_exists


@click.group(name='users')
def users(*args, **kwargs):
    pass


@users.command(name='create')
@authenticated
@click.option('--fullname', prompt='Full Name', callback=validate_name)
@click.option('--email', prompt='Email', callback=validate_email)
@click.option('--password', prompt='Password', hide_input=True, callback=validate_password)
@orm
def _create(session, fullname, email, password, *args, **kwargs):
    user = session.scalars(select(User).where(User.email == email).limit(1)).first()
    if user:
        return display_user_exists(user)
    user = User(
        fullname=fullname,
        email=email,
    )
    user.set_password(password)
    session.add(user)
    session.commit()
    return display_user(user, separator=True)


@users.command(name='list')
@authenticated
@orm
def _list(session: Session, *args, **kwargs):
    user_list = session.scalars(select(User)).all()
    return display_users(user_list)


@users.command(name='delete')
@click.option('--id', 'uid', prompt='Id', type=int)
@orm
def _delete(session: Session, uid, *args, **kwargs):
    user = session.scalars(select(User).where(User.id == uid).limit(1)).first()
    if not user:
        return display_user_not_exists()
    session.delete(user)
    session.commit()
    return display_user_deletion(user)
