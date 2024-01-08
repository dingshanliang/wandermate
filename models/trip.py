from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from db.session import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Trip(Base):
    """
    行程ID (TripID)
    创建者ID (CreatorID)
    行程标题 (Title)
    行程描述 (Description)
    行程开始时间 (StartTime)
    行程结束时间 (EndTime)
    行程天气信息 (WeatherInfo)
    行程公开状态 (PublicStatus)
    """
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    weather_info = Column(String)
    public_status = Column(Boolean)

    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="trips")
