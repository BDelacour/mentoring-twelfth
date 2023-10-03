import click

from python_p12.controllers.user import users


@click.group(name='cli')
def cli():
    pass

cli.add_command(users)
