import datetime
from unittest import mock

import jwt
from _pytest.fixtures import fixture
from dotenv import load_dotenv

from epic_events.auth import _get_secret
from epic_events.models.role import Role, Roles
from epic_events.models.user import User

load_dotenv()


@fixture
def user_password():
    return "MyP@ssW0rd1sH4rd"


@fixture
def fake_user(user_password):
    role = Role(
        id=1,
        name=Roles.SALE.name
    )

    user = User(
        id=1,
        fullname='John Doe',
        email='jdoe@email.com',
        role_id=role.id,
        role=role,
        creation_date=datetime.datetime.utcnow(),
        update_date=datetime.datetime.utcnow(),
    )
    user.set_password(user_password)
    return user


@fixture
def fake_users(fake_user, user_password):
    support_role = Role(
        id=2,
        name=Roles.SUPPORT.name
    )
    management_role = Role(
        id=3,
        name=Roles.MANAGEMENT.name
    )

    user2 = User(
        id=2,
        fullname='Marie Doe',
        email='mdoe@email.com',
        role_id=management_role.id,
        role=management_role,
        creation_date=datetime.datetime.utcnow(),
        update_date=datetime.datetime.utcnow(),
    )
    user2.set_password(user_password)

    user3 = User(
        id=3,
        fullname='Alvin Doe',
        email='adoe@email.com',
        role_id=support_role.id,
        role=support_role,
        creation_date=datetime.datetime.utcnow(),
        update_date=datetime.datetime.utcnow(),
    )
    user3.set_password(user_password)
    return [fake_user, user2, user3]


@fixture
def fake_session():
    return mock.MagicMock()


@fixture
def fake_context(fake_session):
    context = mock.MagicMock()
    context.obj = {
        'session': fake_session
    }
    return context


@fixture
def fake_token(fake_user):
    return jwt.encode({"uid": fake_user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)},
                      _get_secret(), algorithm="HS256")
