from typing import List

import click

from epic_events.models.client import Client
from epic_events.validators import validate_name, validate_email, validate_phone_number


def display_client(client: Client, separator: bool = False):
    if separator:
        print("---")
    print(f"Id : {client.id}\n"
          f"Fullname : {client.fullname}\n"
          f"Email : {client.email}\n"
          f"Phone Number : {client.phone_number}\n"
          f"Company : {client.company_name}\n"
          f"Sale User : {client.sale_user.fullname} ({client.sale_user.email})")


def display_clients(client_list: List[Client]):
    for i, client in enumerate(client_list):
        display_client(client, separator=i > 0)


def display_client_exists(client: Client):
    raise click.ClickException(f"Client \"{client.email}\" already exists")


def display_client_not_exists():
    raise click.ClickException('Requested client does not exist')


def display_client_deletion(client: Client):
    print(f"Client \"{client.email}\" [uid={client.id}] successfully deleted")


def ask_for_client_update(client: Client):
    print("Will modify the following client")
    display_client(client)
    print("---\nLeave empty for same")

    fullname = input("Full name : ") or None
    if fullname:
        validate_name(None, "fullname", fullname)

    email = input("Email : ") or None
    if email:
        validate_email(None, "email", email)

    phone_number = input("Phone Number : ") or None
    if phone_number:
        validate_phone_number(None, "phone_number", phone_number)

    company = input("Company : ") or None
    if company:
        validate_name(None, "company", company)

    sale_user_id = input("Sale User Id : ") or None
    if sale_user_id:
        if not sale_user_id.isdigit():
            raise click.ClickException('Invalid id')
        sale_user_id = int(sale_user_id)

    return {
        'fullname': fullname,
        'email': email,
        'phone_number': phone_number,
        'company': company,
        'sale_user_id': sale_user_id
    }
