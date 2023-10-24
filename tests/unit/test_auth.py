import datetime
import os
from unittest import mock

import jwt
import pytest

from epic_events.auth import authenticate, _get_secret, clear_authentication, auth_middleware

expected_filepath = os.path.join(os.path.expanduser("~"), ".epicevents", "user.key")


def test_authenticate(fake_user):
    expected_expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)

    with mock.patch('epic_events.auth.open', mock.mock_open()) as mock_fp:
        authenticate(fake_user)
    mock_fp.assert_called_with(expected_filepath, 'w')
    mock_fp.return_value.write.assert_called_once()

    token = mock_fp.return_value.write.call_args[0][0]
    payload = jwt.decode(token, _get_secret(), algorithms=["HS256"])
    assert payload["uid"] == fake_user.id
    assert datetime.datetime.utcfromtimestamp(payload["exp"]) - expected_expiration < datetime.timedelta(seconds=5)


@pytest.mark.parametrize("exists,is_file",
                         [
                             (False, False),
                             (False, True),
                             (True, False),
                             (True, True),
                         ])
def test_clear_authentication(exists, is_file):
    with mock.patch('epic_events.auth.os') as mock_os:
        mock_os.path.exists.return_value = exists
        mock_os.path.isfile.return_value = is_file

        clear_authentication()

        mock_os.path.exists.assert_called_once_with(expected_filepath)
        if exists:
            mock_os.path.isfile.assert_called_once_with(expected_filepath)
        else:
            mock_os.path.isfile.assert_not_called()
        if exists and is_file:
            mock_os.unlink.assert_called_once_with(expected_filepath)
        else:
            mock_os.unlink.assert_not_called()


@pytest.mark.parametrize("file_exists,file_isfile,valid_token,user_exists",
                         [
                             (False, False, True, True),
                             (True, False, True, True),
                             (True, True, False, True),
                             (True, True, True, False),
                             (True, True, True, True),
                         ])
def test_auth_middleware(fake_context, fake_user, fake_token, file_exists, file_isfile, valid_token, user_exists):
    token = 'INV.AL.ID'
    if valid_token:
        token = fake_token

    session = fake_context.obj['session']
    session.scalar.return_value = None
    if user_exists:
        session.scalar.return_value = fake_user

    success = file_exists and file_isfile and valid_token and user_exists

    with mock.patch('epic_events.auth.os') as mock_os, \
            mock.patch('epic_events.auth.open', mock.mock_open(read_data=token)) as mock_fp:
        mock_os.path.exists.return_value = file_exists
        mock_os.path.isfile.return_value = file_isfile

        wrapper = auth_middleware(lambda a: None)
        wrapper(fake_context)

        mock_os.path.exists.assert_called_once_with(expected_filepath)
        if file_exists:
            mock_os.path.isfile.assert_called_once_with(expected_filepath)
            if file_isfile:
                mock_fp.assert_called_once_with(expected_filepath, 'r')
                if valid_token:
                    session.scalar.assert_called_once()
                    scalar_call_args = session.scalar.call_args[0]
                    assert len(scalar_call_args) == 1
                    select = scalar_call_args[0]
                    assert str(select) == "SELECT users.id, users.fullname, users.email, users.password_hash, users.role_id, users.creation_date, users.update_date \nFROM users \nWHERE users.id = :id_1"

        if success:
            assert 'user' in fake_context.obj
            user = fake_context.obj['user']
            assert user is not None
        else:
            assert 'user' not in fake_context.obj
