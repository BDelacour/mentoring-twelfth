from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from epic_events.models.base import Base


def orm_middleware(func):
    def wrapper(ctx, *args, **kwargs):
        ctx.ensure_object(dict)

        engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')

        Base.metadata.bind = engine

        SessionMaker: sessionmaker[Session] = sessionmaker(bind=engine)
        with SessionMaker() as session:
            ctx.obj['session'] = session
            return func(ctx, *args, **kwargs)
    return wrapper
