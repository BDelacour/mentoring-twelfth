from typing import List

import click

from epic_events.models.contract import Contract
from epic_events.validators import validate_name, validate_email, validate_phone_number


def display_contract(contract: Contract, separator: bool = False):
    if separator:
        print("---")
    print(f"Id : {contract.id}\n"
          f"Client : {contract.client.fullname} ({contract.client.email})\n"
          f"Sale User : {contract.sale_user.fullname} ({contract.sale_user.email})\n"
          f"Total Amount : {contract.total_amount}\n"
          f"Remaining Amount : {contract.remaining_amount}\n"
          f"Signed : {contract.is_signed}")


def display_contracts(contract_list: List[Contract]):
    for i, contract in enumerate(contract_list):
        display_contract(contract, separator=i > 0)


def display_contract_not_exists():
    raise click.ClickException('Requested contract does not exist')


def display_contract_deletion(contract: Contract):
    print(f"Contract [uid={contract.id}] successfully deleted")


def ask_for_contract_update(contract: Contract):
    print("Will modify the following contract")
    display_contract(contract)
    print("---\nLeave empty for same")

    client_id = input("Client Id : ") or None
    if client_id:
        if not client_id.isdigit():
            raise click.ClickException('Invalid client id')
        client_id = int(client_id)

    sale_user_id = input("Sale User Id : ") or None
    if sale_user_id:
        if not sale_user_id.isdigit():
            raise click.ClickException('Invalid sale user id')
        sale_user_id = int(sale_user_id)

    total_amount = input("Total Amount : ") or None
    if total_amount:
        if not total_amount.isdigit():
            raise click.ClickException('Invalid total amount')
        total_amount = int(total_amount)

    remaining_amount = input("Remaining Amount : ") or None
    if remaining_amount:
        if not remaining_amount.isdigit():
            raise click.ClickException('Invalid total amount')
        remaining_amount = int(remaining_amount)

    is_signed = input("Signed (yes/no) : ") or None
    if is_signed:
        is_signed = is_signed.lower()
        if is_signed in ["y", "yes"]:
            is_signed = True
        elif is_signed in ["n", "no"]:
            is_signed = False
        else:
            raise click.ClickException('Invalid signed')

    return {
        'client_id': client_id,
        'sale_user_id': sale_user_id,
        'total_amount': total_amount,
        'remaining_amount': remaining_amount,
        'is_signed': is_signed
    }
