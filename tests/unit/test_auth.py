import datetime
import os
from unittest import mock

import jwt
import pytest

from epic_events.auth import authenticate, SECRET, clear_authentication


def test_authenticate(fake_user):
    expected_filepath = os.path.join(os.path.expanduser("~"), ".epicevents", "user.key")
    expected_expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)

    with mock.patch('epic_events.auth.open', mock.mock_open()) as mock_fp:
        authenticate(fake_user)
    mock_fp.assert_called_with(expected_filepath, 'w')
    mock_fp.return_value.write.assert_called_once()

    token = mock_fp.return_value.write.call_args[0][0]
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
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
    expected_filepath = os.path.join(os.path.expanduser("~"), ".epicevents", "user.key")

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
