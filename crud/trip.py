from typing import List

from fastapi.encoders import jsonable_encoder

from crud.base import CRUDBase
from models import Trip
from schemas import TripCreate, TripUpdate


class CRUDTrip(CRUDBase[Trip, TripCreate, TripUpdate]):

    # 通过创建者id查询所有行程
    def get_by_creator_id(self, db, *, creator_id: int) -> List[Trip]:
        return db.query(Trip).filter(Trip.creator_id == creator_id).all()

    # 通过参与人id查询所有行程
    def get_by_participant_id(self, db, *, participant_id: int):
        return db.query(Trip).filter(Trip.participants.any(id=participant_id)).all()

    # 通过创建者ID创建行程
    def create_with_creator_id(self, db, *, obj_in: TripCreate, creator_id: int):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Trip(**obj_in_data, creator_id=creator_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


trip = CRUDTrip(Trip)
