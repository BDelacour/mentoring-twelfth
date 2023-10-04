import click
from sqlalchemy import select

from python_p12.models.user import User
from python_p12.permissions import permission, IsAuthenticated
from python_p12.validators import validate_email, validate_password, validate_name
from python_p12.views.users import display_users, display_user, display_user_deletion, display_user_exists, \
    display_user_not_exists


@click.group(name='users')
@click.pass_context
@permission([IsAuthenticated])
def users(ctx, *args, **kwargs):
    pass


@users.command(name='create',
               params=[
                   click.Option(('--fullname',), prompt='Full Name', callback=validate_name),
                   click.Option(('--email',), prompt='Email', callback=validate_email),
                   click.Option(('--password',), prompt='Password', hide_input=True, callback=validate_password),
               ])
@click.pass_context
def _create(ctx, fullname, email, password, *args, **kwargs):
    session = ctx.obj['session']
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
@click.pass_context
def _list(ctx, *args, **kwargs):
    session = ctx.obj['session']
    user_list = session.scalars(select(User)).all()
    return display_users(user_list)


@users.command(name='delete',
               params=[
                   click.Option(('--id', 'uid',), prompt='Id', type=int)
               ])
@click.pass_context
def _delete(ctx, uid, *args, **kwargs):
    session = ctx.obj['session']
    user = session.scalars(select(User).where(User.id == uid).limit(1)).first()
    if not user:
        return display_user_not_exists()
    session.delete(user)
    session.commit()
    return display_user_deletion(user)
