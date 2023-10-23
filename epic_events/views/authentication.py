import click


def display_login_error():
    raise click.ClickException('Login failed')


def display_login_success():
    print('You successfully logged in !')
