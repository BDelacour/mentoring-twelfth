from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped

from epic_events.models.base import Base, utcnow
from epic_events.models.client import Client
from epic_events.models.contract import Contract
from epic_events.models.user import User


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = Column(Integer, primary_key=True)
    contract_id: Mapped[int] = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    client_id: Mapped[int] = Column(Integer, ForeignKey('clients.id'), nullable=False)
    support_user_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_date: Mapped[DateTime] = Column(DateTime, nullable=False)
    end_date: Mapped[DateTime] = Column(DateTime, nullable=False)
    location: Mapped[str] = Column(String(128), nullable=False)
    attendees: Mapped[int] = Column(Integer, nullable=False)
    notes: Mapped[str] = Column(Text, nullable=False)
    creation_date: Mapped[DateTime] = Column(DateTime, server_default=utcnow(), nullable=False)
    update_date: Mapped[DateTime] = Column(DateTime, server_default=utcnow(), onupdate=utcnow(), nullable=False)

    contract: Mapped[Contract] = relationship('Contract', back_populates='events')
    client: Mapped[Client] = relationship('Client', back_populates='events')
    support_user: Mapped[User] = relationship('User', back_populates='events')
