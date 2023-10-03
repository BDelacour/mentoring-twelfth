from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from python_p12.models.base import Base


def orm(func):
    def wrapper(*args, **kwargs):
        engine = create_engine('sqlite:///mydatabase.db')

        Base.metadata.create_all(engine)

        SessionMaker: sessionmaker[Session] = sessionmaker(bind=engine)
        session = SessionMaker()

        result = func(session, *args, **kwargs)
        session.commit()
        return result
    return wrapper
