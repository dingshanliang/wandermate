from typing import List

from fastapi.encoders import jsonable_encoder

from crud.base import CRUDBase
from models import Trip, Invitation
from schemas import TripCreate, TripUpdate


class CRUDTrip(CRUDBase[Trip, TripCreate, TripUpdate]):

    # 通过创建者id查询所有行程,也就是获得我所创建的所有行程
    def get_by_creator_id(self, db, *, creator_id: int) -> List[Trip]:
        return db.query(Trip).filter(Trip.creator_id == creator_id).all()

    # 通过参与人id查询所有行程(也就是获得我所有被邀请的行程)
    def get_by_invitee_id(self, db, *, invitee_id: int):
        # 先通过 invitee_id 在 invitations 表中查出所有的trip_id
        trip_ids = db.query(Invitation.trip_id).filter(Invitation.invitee_id == invitee_id).all()
        trip_ids = [trip_id[0] for trip_id in trip_ids]
        # 再通过 trip_ids 在 trips 表中查出所有的 trip
        return db.query(Trip).filter(Trip.id.in_(trip_ids)).all()

    # 通过创建者ID创建行程
    def create_with_creator_id(self, db, *, obj_in: TripCreate, creator_id: int):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Trip(**obj_in_data, creator_id=creator_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


trip = CRUDTrip(Trip)
