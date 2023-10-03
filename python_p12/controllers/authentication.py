import click
from sqlalchemy import select

from python_p12.database import orm
from python_p12.auth import authenticate, clear_authentication
from python_p12.models.user import User
from python_p12.validators import validate_email, validate_password
from python_p12.views.authentication import display_login_error, display_login_success


@click.command(name='login')
@click.option('--email', prompt='Email', callback=validate_email)
@click.option('--password', prompt='Password', hide_input=True, callback=validate_password)
@orm
def login(session, email, password, *args, **kwargs):
    user = session.scalars(select(User).where(User.email == email).limit(1)).first()
    if user is None:
        return display_login_error()
    if not user.check_password(password):
        return display_login_error()
    authenticate(user)
    return display_login_success()


@click.command(name='logout')
def logout(*args, **kwargs):
    clear_authentication()
