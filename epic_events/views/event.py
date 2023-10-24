from datetime import datetime
from typing import List

import click

from epic_events.models.event import Event
from epic_events.validators import validate_name


def display_event(event: Event, separator: bool = False):
    if separator:
        print("---")
    print(f"Id : {event.id}\n"
          f"Contract Id : {event.contract_id}\n"
          f"Client : {event.contract.client.fullname} ({event.contract.client.email})\n"
          f"Support User : {event.support_user.fullname} ({event.support_user.email})\n"
          f"Start Date : {event.start_date.strftime('%d/%m/%Y')}\n"
          f"End Date : {event.end_date.strftime('%d/%m/%Y')}\n"
          f"Location : {event.location}\n"
          f"Attendees : {event.attendees}\n"
          f"Notes : {event.notes}")


def display_events(event_list: List[Event]):
    for i, event in enumerate(event_list):
        display_event(event, separator=i > 0)


def display_event_not_exists():
    raise click.ClickException('Requested event does not exist')


def display_contract_not_signed():
    raise click.ClickException('Contract must be signed to create event')


def display_event_deletion(event: Event):
    print(f"Event [uid={event.id}] successfully deleted")


def ask_for_event_update(event: Event):
    print("Will modify the following event")
    display_event(event)
    print("---\nLeave empty for same")

    contract_id = input("Contract Id : ") or None
    if contract_id:
        if not contract_id.isdigit():
            raise click.ClickException('Invalid contract id')
        contract_id = int(contract_id)

    start_date = input("Start Date (DD/MM/YYYY) : ") or None
    if start_date:
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        if not start_date:
            raise click.ClickException('Invalid start_date')

    end_date = input("End Date (DD/MM/YYYY) : ") or None
    if end_date:
        end_date = datetime.strptime(end_date, '%d/%m/%Y')
        if not end_date:
            raise click.ClickException('Invalid start_date')

    location = input("Location : ") or None
    if location:
        validate_name(None, None, location)

    attendees = input("Attendees : ") or None
    if attendees:
        if not attendees.isdigit():
            raise click.ClickException('Invalid attendees')
        attendees = int(attendees)

    notes = input("Notes : ") or None

    return {
        'contract_id': contract_id,
        'start_date': start_date,
        'end_date': end_date,
        'location': location,
        'attendees': attendees,
        'notes': notes
    }
