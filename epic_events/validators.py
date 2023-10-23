import re

import click
from sqlalchemy import select

from epic_events.models.client import Client
from epic_events.models.role import Role, Roles
from epic_events.models.user import User


def validate_password(ctx, param, value):
    if len(value) < 12 \
            or not any(char.isdigit() for char in value) \
            or not any(char.islower() for char in value) \
            or not any(char.isupper() for char in value) \
            or value.isalnum():
        raise click.ClickException(
            'Invalid password format (min 12 characters, 1 lowercase, 1 uppercase, 1 digit, 1 symbol)')
    return value


def validate_phone_number(ctx, param, value):
    if len(value) != 10 \
            or not value.isdigit():
        raise click.ClickException('Invalid phone number format')
    return value


def validate_email(ctx, param, value):
    regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
    if not regex.fullmatch(value):
        raise click.ClickException('Invalid email format')
    return value


def validate_name(ctx, param, value):
    if len(value) < 3:
        raise click.ClickException('Invalid name format')
    return value


def validate_role(ctx, param, value):
    role = value.upper()
    if role not in [r.name for r in Roles]:
        raise click.ClickException('Invalid role name')
    return role
