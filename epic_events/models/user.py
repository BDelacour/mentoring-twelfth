from typing import List

import bcrypt
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from epic_events.models.base import Base, utcnow
from epic_events.models.role import Role


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = Column(Integer, primary_key=True)
    fullname: Mapped[str] = Column(String(128), nullable=False)
    email: Mapped[str] = Column(String(320), unique=True, nullable=False)
    password_hash: Mapped[str] = Column(String(60), nullable=False)
    role_id: Mapped[int] = Column(Integer, ForeignKey('roles.id'), nullable=False)
    creation_date: Mapped[DateTime] = Column(DateTime, server_default=utcnow(), nullable=False)
    update_date: Mapped[DateTime] = Column(DateTime, server_default=utcnow(), onupdate=utcnow(), nullable=False)

    role: Mapped[Role] = relationship('Role', back_populates='users')

    clients: Mapped[List['Client']] = relationship('Client', back_populates='sale_user')
    contracts: Mapped[List['Contract']] = relationship('Contract', back_populates='sale_user')
    events: Mapped[List['Event']] = relationship('Event', back_populates='support_user')

    def set_password(self, password: str) -> None:
        # Hash the password and store the hash
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password_hash = password_hash.decode('utf-8')

    def check_password(self, password: str) -> bool:
        # Check if the provided password matches the stored hash
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
