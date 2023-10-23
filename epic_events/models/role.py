from enum import Enum
from typing import List

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship, Mapped

from epic_events.models.base import Base, utcnow


class Roles(Enum):
    SALE = 1,
    SUPPORT = 2,
    MANAGEMENT = 3


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(32), nullable=False)
    creation_date: Mapped[DateTime] = Column(DateTime, server_default=utcnow(), nullable=False)
    update_date: Mapped[DateTime] = Column(DateTime, server_default=utcnow(), onupdate=utcnow(), nullable=False)

    users: Mapped[List['User']] = relationship('User', back_populates='role')
