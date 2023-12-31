import click
from sqlalchemy import select

from epic_events.models.client import Client
from epic_events.models.contract import Contract
from epic_events.models.role import Roles
from epic_events.permissions import permission, IsAuthenticated, IsRolePerson
from epic_events.views.client import display_client_not_exists
from epic_events.views.contract import display_contract, display_contract_not_exists, ask_for_contract_update, \
    display_contracts, display_contract_deletion


@click.group(name='contracts')
@click.pass_context
@permission([IsAuthenticated()])
def contracts(ctx, *args, **kwargs):
    pass


@contracts.command(name='create')
@click.option('--client-id', 'cid', prompt='Client Id', type=click.IntRange(1))
@click.option('--amount', prompt='Amount', type=click.IntRange(0))
@click.pass_context
@permission([IsRolePerson(Roles.MANAGEMENT)])
def _create(ctx, cid, amount, *args, **kwargs):
    session = ctx.obj['session']
    client = session.scalar(select(Client).where(Client.id == cid))
    if not client:
        return display_client_not_exists()

    contract = Contract(
        client=client,
        total_amount=amount,
        remaining_amount=amount,
        is_signed=False
    )
    session.add(contract)
    session.commit()
    return display_contract(contract, separator=True)


@contracts.command(name='update')
@click.option('--id', 'cid', prompt='Id', type=click.IntRange(1))
@click.pass_context
@permission([IsRolePerson(Roles.MANAGEMENT)])
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
@click.option('--id', 'cid', prompt='Id', type=click.IntRange(1))
@click.pass_context
@permission([IsRolePerson(Roles.MANAGEMENT)])
def _delete(ctx, cid, *args, **kwargs):
    session = ctx.obj['session']
    contract = session.scalar(select(Contract).where(Contract.id == cid))
    if not contract:
        return display_contract_not_exists()

    session.delete(contract)
    session.commit()
    return display_contract_deletion(contract)
