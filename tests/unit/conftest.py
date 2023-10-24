from datetime import datetime

from _pytest.fixtures import fixture

from epic_events.models.user import User


@fixture
def fake_user():
    return User(
        id=1,
        fullname='John Doe',
        email='jdoe@email.com',
        password_hash='hashed',
        role_id=1,
        creation_date=datetime.utcnow(),
        update_date=datetime.utcnow(),
    )