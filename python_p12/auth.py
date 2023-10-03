import os

import click
import jwt
from jwt import InvalidTokenError

from python_p12.models.user import User

SECRET = "changeme"

app_token_dir = os.path.join(os.path.expanduser('~'), '.epicevents')
os.makedirs(app_token_dir, exist_ok=True)

token_filepath = os.path.join(app_token_dir, f"user.key")


def authenticate(user: User):
    token = jwt.encode({"uid": user.id}, SECRET, algorithm="HS256")
    clear_authentication()
    with open(token_filepath, 'w') as fp:
        fp.write(token)


def clear_authentication():
    if os.path.exists(token_filepath) and os.path.isfile(token_filepath):
        os.unlink(token_filepath)


def authenticated(func):
    def wrapper(*args, **kwargs):
        if not os.path.exists(token_filepath) or not os.path.isfile(token_filepath):
            raise click.ClickException('Unauthorized')
        with open(token_filepath, 'r') as fp:
            token = fp.read()
        try:
            payload = jwt.decode(token, SECRET, algorithms=["HS256"])
            kwargs['payload'] = payload
        except InvalidTokenError:
            raise click.ClickException('Unauthorized')
        return func(*args, **kwargs)

    return wrapper
