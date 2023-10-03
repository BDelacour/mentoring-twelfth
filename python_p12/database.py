from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from python_p12.models.base import Base


def orm(func):
    def wrapper(*args, **kwargs):
        engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')

        Base.metadata.bind = engine

        SessionMaker: sessionmaker[Session] = sessionmaker(bind=engine)
        with SessionMaker() as session:
            kwargs['session'] = session
            return func(*args, **kwargs)
    return wrapper
