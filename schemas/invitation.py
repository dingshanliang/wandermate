from enum import Enum
from pydantic import BaseModel


class InvitationStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class InvitationBase(BaseModel):
    invitee_id: int
    trip_id: int
    status: InvitationStatus


class InvitationCreate(InvitationBase):
    pass


class InvitationUpdate(InvitationBase):
    pass


class InvitationInDBBase(InvitationBase):
    id: int
    inviter_id: int

    class Config:
        orm_mode = True


class InvitationInDB(InvitationInDBBase):
    pass


class InvitationResponse(InvitationInDBBase):
    pass
