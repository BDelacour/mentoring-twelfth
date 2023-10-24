import functools
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from epic_events.models.base import Base


@functools.cache
def _get_database_url():
    url = os.environ.get('DATABASE_URL')
    assert url
    return url


def orm_middleware(func):
    def wrapper(ctx, *args, **kwargs):
        ctx.ensure_object(dict)

        engine = create_engine(_get_database_url())

        Base.metadata.bind = engine

        SessionMaker: sessionmaker[Session] = sessionmaker(bind=engine)
        with SessionMaker() as session:
            ctx.obj['session'] = session
            return func(ctx, *args, **kwargs)

    return wrapper
