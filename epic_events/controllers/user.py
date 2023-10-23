import click
from sqlalchemy import select

from epic_events.models.user import User
from epic_events.permissions import permission, IsAuthenticated
from epic_events.validators import validate_email, validate_password, validate_name
from epic_events.views.users import display_users, display_user, display_user_deletion, display_user_exists, \
    display_user_not_exists, ask_for_user_update


@click.group(name='users')
@click.pass_context
@permission([IsAuthenticated])
def users(ctx, *args, **kwargs):
    pass


@users.command(name='create')
@click.option('--fullname', prompt='Full Name', callback=validate_name)
@click.option('--email', prompt='Email', callback=validate_email)
@click.option('--password', prompt='Password', hide_input=True, callback=validate_password)
@click.pass_context
def _create(ctx, fullname, email, password, *args, **kwargs):
    session = ctx.obj['session']
    user = session.scalar(select(User).where(User.email == email))
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


@users.command(name='update')
@click.option('--id', 'uid', prompt='Id', type=int)
@click.pass_context
def _update(ctx, uid, *args, **kwargs):
    session = ctx.obj['session']
    user = session.scalar(select(User).where(User.id == uid))
    if not user:
        return display_user_not_exists()

    updated_user_info = ask_for_user_update(user)
    if updated_user_info['fullname'] != "":
        user.fullname = updated_user_info['fullname']
    if updated_user_info['email'] != "":
        user.email = updated_user_info['email']
    if updated_user_info['password'] != "":
        user.set_password(updated_user_info['password'])
    session.add(user)
    session.commit()
    return display_user(user, separator=True)


@users.command(name='list')
@click.pass_context
def _list(ctx, *args, **kwargs):
    session = ctx.obj['session']
    user_list = session.scalars(select(User)).all()
    return display_users(user_list)


@users.command(name='delete')
@click.option('--id', 'uid', prompt='Id', type=int)
@click.pass_context
def _delete(ctx, uid, *args, **kwargs):
    session = ctx.obj['session']
    user = session.scalar(select(User).where(User.id == uid))
    if not user:
        return display_user_not_exists()
    session.delete(user)
    session.commit()
    return display_user_deletion(user)
