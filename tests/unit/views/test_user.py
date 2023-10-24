from unittest import mock

import click
import pytest

from epic_events.models.role import Roles
from epic_events.views.user import display_user_exists, display_user, display_users, display_role_not_exists, \
    display_user_not_exists, display_user_deletion, ask_for_user_update
from tests.unit.conftest import user_password


def test_display_user(fake_user):
    with mock.patch('epic_events.views.user.print') as print_mock:
        display_user(fake_user)
        print_mock.assert_called_once_with(f"Id : {fake_user.id}\n"
                                           f"Fullname : {fake_user.fullname}\n"
                                           f"Email : {fake_user.email}\n"
                                           f"Role : {fake_user.role.name.capitalize()}")


def test_display_users(fake_users):
    with mock.patch('epic_events.views.user.print') as print_mock:
        display_users(fake_users)
        print_mock.assert_has_calls([
            mock.call(f"Id : {fake_users[0].id}\n"
                      f"Fullname : {fake_users[0].fullname}\n"
                      f"Email : {fake_users[0].email}\n"
                      f"Role : {fake_users[0].role.name.capitalize()}"),
            mock.call("---"),
            mock.call(f"Id : {fake_users[1].id}\n"
                      f"Fullname : {fake_users[1].fullname}\n"
                      f"Email : {fake_users[1].email}\n"
                      f"Role : {fake_users[1].role.name.capitalize()}"),
            mock.call("---"),
            mock.call(f"Id : {fake_users[2].id}\n"
                      f"Fullname : {fake_users[2].fullname}\n"
                      f"Email : {fake_users[2].email}\n"
                      f"Role : {fake_users[2].role.name.capitalize()}"),
        ])


def test_display_user_exists(fake_user):
    try:
        display_user_exists(fake_user)
        raise AssertionError()
    except click.ClickException as e:
        assert e.message == f"User \"{fake_user.email}\" already exists"


def test_display_role_not_exists():
    try:
        display_role_not_exists()
        raise AssertionError()
    except click.ClickException as e:
        assert e.message == f"Requested role is not valid ({', '.join([r.name.capitalize() for r in Roles])})"


def test_display_user_not_exists():
    try:
        display_user_not_exists()
        raise AssertionError()
    except click.ClickException as e:
        assert e.message == "Requested user is not valid"


def test_display_user_deletion(fake_user):
    with mock.patch('epic_events.views.user.print') as print_mock:
        display_user_deletion(fake_user)
        print_mock.assert_called_once_with(f"User \"{fake_user.email}\" [uid={fake_user.id}] successfully deleted")


@pytest.mark.parametrize("fullname,fullname_valid,email,email_valid,role,role_valid,password,password_valid,old_password,old_password_valid,expected_result",
                         [
                             ("", True, "", True, "", True, "", True, "", True, {
                                 'fullname': None,
                                 'email': None,
                                 'role': None,
                                 'password': None
                             }),
                             ("JD", False, "", True, "", True, "", True, "", True, None),
                             ("John Dickson", True, "jdickson", False, "", True, "", True, "", True, None),
                             ("John Dickson", True, "jdickson@email.com", True, "unknown", False, "", True, "", True, None),
                             ("John Dickson", True, "jdickson@email.com", True, "SALE", True, "azerty", False, "", True, None),
                             ("John Dickson", True, "jdickson@email.com", True, "SALE", True, "I love to eat 4 potatoes", True, "oldpass", False, None),
                             ("John Dickson", True, "", True, "", True, "", True, "", True, {
                                 'fullname': "John Dickson",
                                 'email': None,
                                 'role': None,
                                 'password': None
                             }),
                             ("", True, "jdickson@email.com", True, "", True, "", True, "", True, {
                                 'fullname': None,
                                 'email': "jdickson@email.com",
                                 'role': None,
                                 'password': None
                             }),
                             ("", True, "", True, "SALE", True, "", True, "", True, {
                                 'fullname': None,
                                 'email': None,
                                 'role': "SALE",
                                 'password': None
                             }),
                             ("", True, "", True, "", True, "I love to eat 4 potatoes", True, "MyP@ssW0rd1sH4rd", True, {
                                 'fullname': None,
                                 'email': None,
                                 'role': None,
                                 'password': "I love to eat 4 potatoes"
                             }),
                             ("John Dickson", True, "jdickson@email.com", True, "SALE", True, "I love to eat 4 potatoes", True, "MyP@ssW0rd1sH4rd", True, {
                                 'fullname': "John Dickson",
                                 'email': "jdickson@email.com",
                                 'role': "SALE",
                                 'password': "I love to eat 4 potatoes"
                             }),
                         ])
def test_ask_for_user_update(fake_user,
                             fullname, fullname_valid,
                             email, email_valid,
                             role, role_valid,
                             password, password_valid,
                             old_password, old_password_valid,
                             expected_result):
    input_return_mapping = {
        'Full Name : ': fullname,
        'Email : ': email,
        'Role : ': role
    }
    getpass_return_mapping = {
        'New password : ': password,
        'Old password : ': old_password
    }
    success = fullname_valid and email_valid and role_valid and password_valid and old_password_valid

    input_calls = [
        mock.call("Full Name : ")
    ]
    getpass_calls = []
    if fullname_valid:
        input_calls.append(mock.call("Email : "))
        if email_valid:
            input_calls.append(mock.call("Role : "))
            if role_valid:
                getpass_calls.append(mock.call("New password : "))
                if password != "" and password_valid:
                    getpass_calls.append(mock.call("Old password : "))

    with mock.patch('epic_events.views.user.print') as print_mock, \
            mock.patch('epic_events.views.user.input') as input_mock, \
            mock.patch('epic_events.views.user.getpass') as getpass_mock:
        input_mock.side_effect = lambda text: input_return_mapping[text]
        getpass_mock.side_effect = lambda text: getpass_return_mapping[text]

        try:
            result = ask_for_user_update(fake_user)
            assert success is True
            assert result == expected_result
        except click.ClickException as e:
            assert success is False

        print_mock.assert_has_calls([
            mock.call("Will modify the following user"),
            mock.call(f"Id : {fake_user.id}\n"
                      f"Fullname : {fake_user.fullname}\n"
                      f"Email : {fake_user.email}\n"
                      f"Role : {fake_user.role.name.capitalize()}"),
            mock.call("---\nLeave empty for same")
        ])
        assert input_mock.call_count == len(input_calls)
        input_mock.assert_has_calls(input_calls)
        assert getpass_mock.call_count == len(getpass_calls)
        getpass_mock.assert_has_calls(getpass_calls)
