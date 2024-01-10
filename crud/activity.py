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
        activity_in_data = jsonable_encoder(activity_in)
        activity_in_data['coordinates'] = coordinates_wkt
        db_activity = Activity(**activity_in_data, creator_id=creator_id, trip_id=trip_id)
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        return db_activity

    # 更新重写，主要是为了转换地理坐标格式
    def update(self, db: Session, *, db_activity: Activity, activity_in: ActivityUpdate) -> Activity:
        # 将坐标数据暂存下来
        coordinates_wkt = db_activity.coordinates
        db_activity.coordinates = None  # 不这么操作就不能对 db_activity 进行jsonable_encoder 操作
        activity_data = jsonable_encoder(db_activity)
        if isinstance(activity_in, dict):
            update_activity = activity_in
        else:
            update_activity = activity_in.dict(exclude_unset=True)

        if update_activity.get('coordinates'):
            update_activity[
                'coordinates'] = f'POINT({activity_in.coordinates.longitude} {activity_in.coordinates.latitude})'
        else:
            update_activity['coordinates'] = coordinates_wkt

        for field in activity_data:
            if field in update_activity:
                setattr(db_activity, field, update_activity[field])

        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        return db_activity


activity = CRUDActivity(Activity)
