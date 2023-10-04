import click
from sqlalchemy import select

from python_p12.auth import authenticate, clear_authentication
from python_p12.models.user import User
from python_p12.validators import validate_email, validate_password
from python_p12.views.authentication import display_login_error, display_login_success


@click.command(name='login',
               params=[
                   click.Option(('--email',), prompt='Email', callback=validate_email),
                   click.Option(('--password',), prompt='Password', hide_input=True, callback=validate_password),
               ])
@click.pass_context
def login(ctx, email, password, *args, **kwargs):
    session = ctx.obj['session']
    user = session.scalar(select(User).where(User.email == email))
    if user is None:
        return display_login_error()
    if not user.check_password(password):
        return display_login_error()
    authenticate(user)
    return display_login_success()


@click.command(name='logout')
@click.pass_context
def logout(ctx, *args, **kwargs):
    clear_authentication()
