from unittest import mock

import click

from epic_events.views.authentication import display_login_error, display_login_success


def test_display_login_error():
    try:
        display_login_error()
        raise AssertionError()
    except click.ClickException as e:
        assert e.message == 'Login failed'


def test_display_login_success():
    with mock.patch('epic_events.views.authentication.print') as print_mock:
        display_login_success()
        print_mock.assert_called_once_with('You successfully logged in !')
