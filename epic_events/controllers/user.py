import click
from sqlalchemy import select

from epic_events.models.role import Role, Roles
from epic_events.models.user import User
from epic_events.permissions import permission, IsAuthenticated, IsRolePerson
from epic_events.validators import validate_email, validate_password, validate_name, validate_role
from epic_events.views.user import display_users, display_user, display_user_deletion, display_user_exists, \
    display_user_not_exists, ask_for_user_update, display_role_not_exists


@click.group(name='users')
@click.pass_context
def users(ctx, *args, **kwargs):
    pass


@users.command(name='create')
@click.option('--fullname', prompt='Full Name', callback=validate_name)
@click.option('--email', prompt='Email', callback=validate_email)
@click.option('--role', prompt='Role', callback=validate_role)
@click.option('--password', prompt='Password', hide_input=True, callback=validate_password)
@click.pass_context
def _create(ctx, fullname, email, role, password, *args, **kwargs):
    session = ctx.obj['session']
    user = session.scalar(select(User).where(User.email == email))
    if user:
        return display_user_exists(user)
    role = session.scalar(select(Role).where(Role.name == role))
    if not role:
        return display_role_not_exists()
    user = User(
        fullname=fullname,
        email=email,
        role=role
    )
    user.set_password(password)
    session.add(user)
    session.commit()
    return display_user(user, separator=True)


@users.command(name='update')
@click.option('--id', 'uid', prompt='Id', type=click.IntRange(1))
@click.pass_context
@permission([IsAuthenticated(), IsRolePerson(Roles.MANAGEMENT)])
def _update(ctx, uid, *args, **kwargs):
    session = ctx.obj['session']
    user = session.scalar(select(User).where(User.id == uid))
    if not user:
        return display_user_not_exists()

    updated_user_info = ask_for_user_update(user)
    if updated_user_info['fullname'] is not None:
        user.fullname = updated_user_info['fullname']
    if updated_user_info['email'] is not None:
        user.email = updated_user_info['email']
    if updated_user_info['role'] is not None:
        role = session.scalar(select(Role).where(Role.name == updated_user_info['role']))
        user.role = role
    if updated_user_info['password'] is not None:
        user.set_password(updated_user_info['password'])
    session.add(user)
    session.commit()
    return display_user(user, separator=True)


@users.command(name='list')
@click.pass_context
@permission([IsAuthenticated()])
def _list(ctx, *args, **kwargs):
    session = ctx.obj['session']
    user_list = session.scalars(select(User)).all()
    return display_users(user_list)


@users.command(name='delete')
@click.option('--id', 'uid', prompt='Id', type=click.IntRange(1))
@click.pass_context
@permission([IsAuthenticated(), IsRolePerson(Roles.MANAGEMENT)])
def _delete(ctx, uid, *args, **kwargs):
    session = ctx.obj['session']
    user = session.scalar(select(User).where(User.id == uid))
    if not user:
        return display_user_not_exists()

    session.delete(user)
    session.commit()
    return display_user_deletion(user)
