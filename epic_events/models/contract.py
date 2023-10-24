from typing import List

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped

from epic_events.models.base import Base, utcnow
from epic_events.models.client import Client
from epic_events.models.user import User


class Contract(Base):
    __tablename__ = 'contracts'

    id: Mapped[int] = Column(Integer, primary_key=True)
    client_id: Mapped[int] = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    total_amount: Mapped[int] = Column(Integer, nullable=False)
    remaining_amount: Mapped[int] = Column(Integer, nullable=False)
    is_signed: Mapped[bool] = Column(Boolean, nullable=False)
    creation_date: Mapped[DateTime] = Column(DateTime, server_default=utcnow(), nullable=False)
    update_date: Mapped[DateTime] = Column(DateTime, server_default=utcnow(), onupdate=utcnow(), nullable=False)

    client: Mapped[Client] = relationship('Client', back_populates='contracts')

    events: Mapped[List['Event']] = relationship('Event', back_populates='contract')
