from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from python_p12.models.base import Base


def orm(func):
    def wrapper(*args, **kwargs):
        engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')

        Base.metadata.create_all(engine)

        SessionMaker: sessionmaker[Session] = sessionmaker(bind=engine)
        with SessionMaker() as session:
            return func(session, *args, **kwargs)
    return wrapper
