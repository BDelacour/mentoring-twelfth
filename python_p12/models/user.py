from typing import List

import bcrypt
from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.orm import relationship, Mapped

from python_p12.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = Column(Integer, primary_key=True)
    fullname: Mapped[str] = Column(String(128), nullable=False)
    email: Mapped[str] = Column(String(320), unique=True, nullable=False)
    password_hash: Mapped[str] = Column(String(60), nullable=False)
    creation_date: Mapped[DateTime] = Column(DateTime, server_default=func.utcnow(), nullable=False)
    update_date: Mapped[DateTime] = Column(DateTime, server_default=func.utcnow(), nullable=False)

    clients: Mapped[List['Client']] = relationship('Client', back_populates='commercial_user')

    def set_password(self, password: str) -> None:
        # Hash the password and store the hash
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password_hash = password_hash.decode('utf-8')

    def check_password(self, password: str) -> bool:
        # Check if the provided password matches the stored hash
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
