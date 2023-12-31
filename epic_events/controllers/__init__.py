import click

from epic_events.auth import auth_middleware
from epic_events.controllers.authentication import login, logout
from epic_events.controllers.client import clients
from epic_events.controllers.contract import contracts
from epic_events.controllers.event import events
from epic_events.controllers.user import users
from epic_events.database import orm_middleware


@click.group(name='cli')
@click.pass_context
@orm_middleware
@auth_middleware
def cli(ctx):
    pass


cli.add_command(users)
cli.add_command(clients)
cli.add_command(contracts)
cli.add_command(events)
cli.add_command(login)
cli.add_command(logout)
