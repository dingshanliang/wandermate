from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, Enum

from db.session import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .trip import Trip  # noqa: F401


class Invitation(Base):

    __tablename__ = 'invitations'

    id = Column(Integer, primary_key=True, index=True)
    inviter_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    invitee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    trip_id = Column(Integer, ForeignKey('trips.id'), nullable=False)
    status = Column(Enum("pending", "accepted", "rejected", name='invitation_status'), nullable=False)
