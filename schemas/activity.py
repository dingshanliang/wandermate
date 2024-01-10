from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel


class Coordinates(BaseModel):
    latitude: float
    longitude: float


class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    coordinates: Optional[Coordinates] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(ActivityBase):
    title: Optional[str] = None


class ActivityInDBBase(ActivityBase):
    id: int
    creator_id: int
    trip_id: int

    class Config:
        orm_mode = True


class ActivityInDB(ActivityInDBBase):
    pass


class ActivityResponse(ActivityInDBBase):
    coordinates: Optional[str] = None
