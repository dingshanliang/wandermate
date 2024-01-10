from fastapi.encoders import jsonable_encoder
from shapely.geometry import Point
from sqlmodel import Session

from crud.base import CRUDBase
from models.activity import Activity
from schemas import ActivityCreate, ActivityUpdate


class CRUDActivity(CRUDBase[Activity, ActivityCreate, ActivityUpdate]):
    # 根据用户id 和 trip id 创建活动
    def create_by_trip_and_user(self, db: Session, *, activity_in: ActivityCreate, creator_id: int,
                                trip_id: int) -> Activity:
        coordinates_wkt = f'POINT({activity_in.coordinates.longitude} {activity_in.coordinates.latitude})' if activity_in.coordinates else None
        # if activity_in.coordinates:
        #     coordinates_wkt = Point(activity_in.coordinates.longitude, activity_in.coordinates.latitude)
        # else:
        #     coordinates_wkt = None
        activity_in_data = jsonable_encoder(activity_in)
        activity_in_data['coordinates'] = coordinates_wkt
        db_activity = Activity(**activity_in_data, creator_id=creator_id, trip_id=trip_id)
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        return db_activity


activity = CRUDActivity(Activity)
