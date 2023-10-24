import click
from sqlalchemy import select

from epic_events.models.contract import Contract
from epic_events.models.event import Event
from epic_events.models.role import Roles, Role
from epic_events.models.user import User
from epic_events.permissions import permission, IsAuthenticated
from epic_events.validators import validate_name
from epic_events.views.contract import display_contract_not_exists
from epic_events.views.event import display_event, display_event_not_exists, ask_for_event_update, display_events, \
    display_event_deletion, display_contract_not_signed
from epic_events.views.user import display_user_not_exists


@click.group(name='events')
@click.pass_context
@permission([IsAuthenticated])
def events(ctx, *args, **kwargs):
    pass


@events.command(name='create')
@click.option('--contract-id', 'cid', prompt='Contract Id', type=click.IntRange(1))
@click.option('--support-user-id', 'suid', prompt='Support User Id', type=click.IntRange(1))
@click.option('--start-date', prompt='Start Date (DD/MM/YYYY)', type=click.DateTime(["%d/%m/%Y"]))
@click.option('--end-date', prompt='End Date (DD/MM/YYYY)', type=click.DateTime(["%d/%m/%Y"]))
@click.option('--location', prompt='Location', callback=validate_name)
@click.option('--attendees', prompt='Attendees', type=click.IntRange(0))
@click.option('--notes', prompt='Notes', type=str)
@click.pass_context
def _create(ctx, cid, suid, start_date, end_date, location, attendees, notes, *args, **kwargs):
    session = ctx.obj['session']
    contract = session.scalar(select(Contract).where(Contract.id == cid))
    if not contract:
        return display_contract_not_exists()
    if not contract.is_signed:
        return display_contract_not_signed()

    support_user = session.scalar(
        select(User)
        .join(User.role)
        .where(User.id == suid)
        .where(Role.name == Roles.SUPPORT.name)
    )
    if not support_user:
        return display_user_not_exists()

    if end_date <= start_date:
        raise click.BadParameter('end_date should be after start_date')

    event = Event(
        contract=contract,
        support_user=support_user,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
    )
    session.add(event)
    session.commit()
    return display_event(event, separator=True)


@events.command(name='update')
@click.option('--id', 'eid', prompt='Id', type=int)
@click.pass_context
def _update(ctx, eid, *args, **kwargs):
    session = ctx.obj['session']
    event = session.scalar(select(Event).where(Event.id == eid))
    if not event:
        return display_event_not_exists()

    updated_event_info = ask_for_event_update(event)
    if updated_event_info['contract_id'] is not None:
        contract = session.scalar(
            select(Contract)
            .where(Contract.id == updated_event_info['contract_id'])
        )
        if not contract:
            return display_contract_not_exists()
        if not contract.is_signed:
            return display_contract_not_signed()
        event.contract = contract
    if updated_event_info['support_user_id'] is not None:
        support_user = session.scalar(
            select(User)
            .join(User.role)
            .where(User.id == updated_event_info['support_user_id'])
            .where(Role.name == Roles.SUPPORT.name)
        )
        if not support_user:
            return display_user_not_exists()
        event.support_user = support_user
    if updated_event_info['start_date'] is not None:
        event.start_date = updated_event_info['start_date']
    if updated_event_info['end_date'] is not None:
        event.end_date = updated_event_info['end_date']
    if updated_event_info['location'] is not None:
        event.location = updated_event_info['location']
    if updated_event_info['attendees'] is not None:
        event.attendees = updated_event_info['attendees']
    if updated_event_info['notes'] is not None:
        event.notes = updated_event_info['notes']

    if event.end_date <= event.start_date:
        raise click.ClickException('end_date should be after start_date')

    session.add(event)
    session.commit()
    return display_event(event, separator=True)


@events.command(name='list')
@click.pass_context
def _list(ctx, *args, **kwargs):
    session = ctx.obj['session']
    event_list = session.scalars(select(Event)).all()
    return display_events(event_list)


@events.command(name='delete')
@click.option('--id', 'eid', prompt='Id', type=int)
@click.pass_context
def _delete(ctx, eid, *args, **kwargs):
    session = ctx.obj['session']
    event = session.scalar(select(Event).where(Event.id == eid))
    if not event:
        return display_event_not_exists()

    session.delete(event)
    session.commit()
    return display_event_deletion(event)
