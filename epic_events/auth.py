import datetime
import functools
import os

import jwt
from jwt import InvalidTokenError
from sqlalchemy import select

from epic_events.models.user import User

app_token_dir = os.path.join(os.path.expanduser("~"), ".epicevents")
os.makedirs(app_token_dir, exist_ok=True)

token_filepath = os.path.join(app_token_dir, "user.key")
token_duration = 3600


@functools.cache
def _get_secret():
    secret = os.environ.get('TOKEN_SECRET')
    assert secret
    return secret


def authenticate(user: User):
    token = jwt.encode({"uid": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=token_duration)},
                       _get_secret(), algorithm="HS256")
    clear_authentication()
    with open(token_filepath, 'w') as fp:
        fp.write(token)


def clear_authentication():
    if os.path.exists(token_filepath) and os.path.isfile(token_filepath):
        os.unlink(token_filepath)


def auth_middleware(func):
    def _get_user_from_token_if_valid(session) -> User | None:
        if not os.path.exists(token_filepath) or not os.path.isfile(token_filepath):
            return None

        with open(token_filepath, 'r') as fp:
            token = fp.read()

        try:
            payload = jwt.decode(token, _get_secret(), algorithms=["HS256"])
        except InvalidTokenError:
            return None
        return session.scalar(select(User).where(User.id == payload['uid']))

    def wrapper(ctx, *args, **kwargs):
        ctx.ensure_object(dict)

        user = _get_user_from_token_if_valid(ctx.obj['session'])
        if user:
            ctx.obj['user'] = user

        return func(ctx, *args, **kwargs)

    return wrapper
