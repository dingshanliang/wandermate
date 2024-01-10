from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.session import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .trip import Trip  # noqa: F401

# 活动ID (ActivityID)
# 行程ID (TripID) [外键关联到行程表]
# 创建者ID (CreatorID) [外键关联到用户表]
# 活动标题 (ActivityTitle)
# 活动描述 (ActivityDescription)
# 活动开始时间 (ActivityStartTime)
# 活动结束时间 (ActivityEndTime)
# 地点ID (LocationID) [外键关联到地点表]

class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey('trips.id'), index=False)
    creator_id = Column(Integer, ForeignKey('users.id'), index=False)
    title = Column(String, index=False)
    description = Column(String, index=False)
    start_time = Column(DateTime, index=False)
    end_time = Column(DateTime, index=False)
    coordinates = Column(Geometry(geometry_type='POINT', srid=4326))

    # 添加关系属性，以便在查询时能够方便地获取关联对象
    trip = relationship('Trip', back_populates='activities')
    creator = relationship('User', back_populates='created_activities')