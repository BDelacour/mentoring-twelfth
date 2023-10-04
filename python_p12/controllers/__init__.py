import click

from python_p12.auth import auth_middleware
from python_p12.controllers.authentication import login, logout
from python_p12.controllers.user import users
from python_p12.database import orm_middleware


@click.group(name='cli')
@click.pass_context
@orm_middleware
@auth_middleware
def cli(ctx):
    pass


cli.add_command(users)
cli.add_command(login)
cli.add_command(logout)
