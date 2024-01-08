from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.session import Base

if TYPE_CHECKING:
    from .trip import Trip     # noqa: F401


class User(Base):
    # table name
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True,unique=True, nullable=False)
    avatar = Column(String)
    phone = Column(String)
    email = Column(String)
    hashed_password = Column(String, nullable=False)

    trips = relationship("Trip", back_populates="creator")



