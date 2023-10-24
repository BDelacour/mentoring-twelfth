import click
from sqlalchemy import select

from epic_events.models.client import Client
from epic_events.models.contract import Contract
from epic_events.models.role import Roles, Role
from epic_events.models.user import User
from epic_events.permissions import permission, IsAuthenticated
from epic_events.views.client import display_client_not_exists
from epic_events.views.contract import display_contract, display_contract_not_exists, ask_for_contract_update, \
    display_contracts, display_contract_deletion
from epic_events.views.user import display_user_not_exists


@click.group(name='contracts')
@click.pass_context
@permission([IsAuthenticated])
def contracts(ctx, *args, **kwargs):
    pass


@contracts.command(name='create')
@click.option('--client-id', 'cid', prompt='Client Id', type=int)
@click.option('--sale-user-id', 'suid', prompt='Sale User Id', type=int)
@click.option('--amount', prompt='Amount', type=int)
@click.pass_context
def _create(ctx, cid, suid, amount, *args, **kwargs):
    session = ctx.obj['session']
    client = session.scalar(select(Client).where(Client.id == cid))
    if not client:
        return display_client_not_exists()

    sale_user = session.scalar(
        select(User)
        .join(User.role)
        .where(User.id == suid)
        .where(Role.name == Roles.SALE.name)
    )
    if not sale_user:
        return display_user_not_exists()

    contract = Contract(
        client=client,
        sale_user=sale_user,
        total_amount=amount,
        remaining_amount=amount,
        is_signed=False
    )
    session.add(contract)
    session.commit()
    return display_contract(contract, separator=True)


@contracts.command(name='update')
@click.option('--id', 'cid', prompt='Id', type=int)
@click.pass_context
def _update(ctx, cid, *args, **kwargs):
    session = ctx.obj['session']
    contract = session.scalar(select(Contract).where(Contract.id == cid))
    if not contract:
        return display_contract_not_exists()

    updated_contract_info = ask_for_contract_update(contract)
    if updated_contract_info['client_id'] is not None:
        client = session.scalar(
            select(Client)
            .where(Client.id == updated_contract_info['client_id'])
        )
        if not client:
            return display_client_not_exists()
        contract.client = client
    if updated_contract_info['sale_user_id'] is not None:
        sale_user = session.scalar(
            select(User)
            .join(User.role)
            .where(User.id == updated_contract_info['sale_user_id'])
            .where(Role.name == Roles.SALE.name)
        )
        if not sale_user:
            return display_user_not_exists()
        contract.sale_user = sale_user
    if updated_contract_info['total_amount'] is not None:
        contract.total_amount = updated_contract_info['total_amount']
    if updated_contract_info['remaining_amount'] is not None:
        contract.remaining_amount = updated_contract_info['remaining_amount']
    if updated_contract_info['is_signed'] is not None:
        contract.is_signed = updated_contract_info['is_signed']

    session.add(contract)
    session.commit()
    return display_contract(contract, separator=True)


@contracts.command(name='list')
@click.pass_context
def _list(ctx, *args, **kwargs):
    session = ctx.obj['session']
    contract_list = session.scalars(select(Contract)).all()
    return display_contracts(contract_list)


@contracts.command(name='delete')
@click.option('--id', 'cid', prompt='Id', type=int)
@click.pass_context
def _delete(ctx, cid, *args, **kwargs):
    session = ctx.obj['session']
    contract = session.scalar(select(Contract).where(Contract.id == cid))
    if not contract:
        return display_contract_not_exists()

    session.delete(contract)
    session.commit()
    return display_contract_deletion(contract)
