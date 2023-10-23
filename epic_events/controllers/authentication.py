import click
from sqlalchemy import select

from epic_events.auth import authenticate, clear_authentication
from epic_events.models.user import User
from epic_events.validators import validate_email, validate_password
from epic_events.views.authentication import display_login_error, display_login_success


@click.command(name='login')
@click.option('--email', prompt='Email', callback=validate_email)
@click.option('--password', prompt='Password', hide_input=True, callback=validate_password)
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
