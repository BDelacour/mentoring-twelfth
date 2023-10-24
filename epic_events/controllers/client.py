import click
from sqlalchemy import select

from epic_events.models.client import Client
from epic_events.models.role import Roles, Role
from epic_events.models.user import User
from epic_events.permissions import permission, IsAuthenticated, IsRolePerson
from epic_events.validators import validate_email, validate_name, validate_phone_number
from epic_events.views.client import display_client, ask_for_client_update, display_clients, display_client_deletion, \
    display_client_not_exists
from epic_events.views.user import display_user_not_exists


@click.group(name='clients')
@click.pass_context
@permission([IsAuthenticated()])
def clients(ctx, *args, **kwargs):
    pass


@clients.command(name='create')
@click.option('--fullname', prompt='Full Name', callback=validate_name)
@click.option('--email', prompt='Email', callback=validate_email)
@click.option('--phone-number', prompt='Phone Number', callback=validate_phone_number)
@click.option('--company', prompt='Company', callback=validate_name)
@click.pass_context
@permission([IsRolePerson(Roles.SALE)])
def _create(ctx, fullname, email, phone_number, company, *args, **kwargs):
    session = ctx.obj['session']
    user = ctx.obj['user']

    client = Client(
        fullname=fullname,
        email=email,
        phone_number=phone_number,
        company_name=company,
        sale_user=user,
    )
    session.add(client)
    session.commit()
    return display_client(client, separator=True)


@clients.command(name='update')
@click.option('--id', 'cid', prompt='Id', type=int)
@click.pass_context
@permission([IsRolePerson(Roles.SALE)])
def _update(ctx, cid, *args, **kwargs):
    session = ctx.obj['session']
    client = session.scalar(select(Client).where(Client.id == cid))
    if not client:
        return display_client_not_exists()

    updated_client_info = ask_for_client_update(client)
    if updated_client_info['fullname'] is not None:
        client.fullname = updated_client_info['fullname']
    if updated_client_info['email'] is not None:
        client.email = updated_client_info['email']
    if updated_client_info['phone_number'] is not None:
        client.phone_number = updated_client_info['phone_number']
    if updated_client_info['company'] is not None:
        client.company_name = updated_client_info['company']
    if updated_client_info['sale_user_id'] is not None:
        sale_user = session.scalar(
            select(User)
            .join(User.role)
            .where(User.id == updated_client_info['sale_user_id'])
            .where(Role.name == Roles.SALE.name)
        )
        if not sale_user:
            return display_user_not_exists()
        client.sale_user = sale_user

    session.add(client)
    session.commit()
    return display_client(client, separator=True)


@clients.command(name='list')
@click.pass_context
def _list(ctx, *args, **kwargs):
    session = ctx.obj['session']
    client_list = session.scalars(select(Client)).all()
    return display_clients(client_list)


@clients.command(name='delete')
@click.option('--id', 'cid', prompt='Id', type=int)
@click.pass_context
@permission([IsRolePerson(Roles.MANAGEMENT)])
def _delete(ctx, cid, *args, **kwargs):
    session = ctx.obj['session']
    client = session.scalar(select(Client).where(Client.id == cid))
    if not client:
        return display_client_not_exists()

    session.delete(client)
    session.commit()
    return display_client_deletion(client)
