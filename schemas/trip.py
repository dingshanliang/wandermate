from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TripBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    weather_info: Optional[str] = None
    public_status: bool


class TripCreate(TripBase):
    pass


class TripUpdate(TripBase):
    pass


class TripInDBBase(TripBase):
    id: int
    creator_id: int

    class Config:
        orm_mode = True


class TripInDB(TripInDBBase):
    pass


class TripResponse(TripInDBBase):
    pass
