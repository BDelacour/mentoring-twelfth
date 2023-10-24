import click
import pytest

from epic_events.validators import validate_password, validate_phone_number, validate_email, validate_name, \
    validate_role


@pytest.mark.parametrize("password,success",
                         [
                             ("", False),  # Too short
                             ("a1B!", False),  # Too short
                             ("I eat apples at school", False),  # Missing digit
                             ("4 plus 4 makes 12", False),  # Missing uppercase
                             ("I TOLD YOU TO STOP 2 TIMES", False),  # Missing lowercase
                             ("YouShallNot4Pass", False),  # Missing symbol
                             ("Sometimes, I like running 10 minutes", True),
                         ])
def test_validate_password(password, success):
    try:
        validate_password(None, None, password)
        assert success is True
    except click.ClickException as e:
        assert success is False


@pytest.mark.parametrize("phone_number,success",
                         [
                             ("06", False),  # Too short
                             ("a1B!0d7z7c", False),  # Not only digit
                             ("0612345678", True),
                         ])
def test_validate_phone_number(phone_number, success):
    try:
        validate_phone_number(None, None, phone_number)
        assert success is True
    except click.ClickException as e:
        assert success is False


@pytest.mark.parametrize("email,success",
                         [
                             ("john.doe", False),  # Missing domain
                             ("john.doe@tld", False),  # Missing extension
                             ("john.doe@email.com", True),
                             ("john.doe+spambox@email.com", True),
                         ])
def test_validate_email(email, success):
    try:
        validate_email(None, None, email)
        assert success is True
    except click.ClickException as e:
        assert success is False


@pytest.mark.parametrize("name,success",
                         [
                             ("JD", False),  # Too short
                             ("John Doe", True),
                         ])
def test_validate_name(name, success):
    try:
        validate_name(None, None, name)
        assert success is True
    except click.ClickException as e:
        assert success is False


@pytest.mark.parametrize("role,success",
                         [
                             ("admin", False),  # Unknown
                             ("sale", True),  # Converted to upper
                             ("Management", True),  # Converted to upper
                             ("SUPPORT", True),  # Converted to upper
                         ])
def test_validate_role(role, success):
    try:
        validate_role(None, None, role)
        assert success is True
    except click.ClickException as e:
        assert success is False
