from typing import List

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from epic_events.models.base import Base, utcnow
from epic_events.models.user import User


class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = Column(Integer, primary_key=True)
    fullname: Mapped[str] = Column(String(128), nullable=False)
    email: Mapped[str] = Column(String(320), nullable=False)
    phone_numer: Mapped[str] = Column(String(32), nullable=False)
    company_name: Mapped[str] = Column(String(64), nullable=False)
    commercial_user_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), nullable=False)
    creation_date: Mapped[DateTime] = Column(DateTime, server_default=utcnow(), nullable=False)
    update_date: Mapped[DateTime] = Column(DateTime, server_default=utcnow(), onupdate=utcnow(), nullable=False)

    commercial_user: Mapped[User] = relationship('User', back_populates='clients')

    contracts: Mapped[List['Contract']] = relationship('Contract', back_populates='client')
    events: Mapped[List['Event']] = relationship('Event', back_populates='client')