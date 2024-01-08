from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from api.deps import get_current_user, get_db

router = APIRouter()


# 获取我创建的所有trip
@router.get("/", response_model=List[schemas.TripResponse])
def get_trips(
        *,
        db: Session = Depends(get_db),
        current_user: schemas.UserResponse = Depends(get_current_user)
):
    trips = crud.trip.get_by_creator_id(db, creator_id=current_user.id)
    return trips


# 创建一个trip
@router.post("/", response_model=schemas.TripResponse)
def create_trip(
        *,
        db: Session = Depends(get_db),
        trip_in: schemas.TripCreate,
        current_user: schemas.UserResponse = Depends(get_current_user)
):
    trip = crud.trip.create_with_creator_id(db, obj_in=trip_in, creator_id=current_user.id)
    return trip


# 更新一个trip
@router.put("/{trip_id}", response_model=schemas.TripResponse)
def update_trip(
        *,
        db: Session = Depends(get_db),
        trip_id: int,
        trip_in: schemas.TripUpdate,
        current_user: schemas.UserResponse = Depends(get_current_user)
):
    trip = crud.trip.get(db, id=trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    # 只有trip的创建者才能更新trip
    if trip.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    trip = crud.trip.update(db, db_obj=trip, obj_in=trip_in)
    return trip


# 删除一个trip
@router.delete("/{trip_id}", response_model=schemas.TripResponse)
def delete_trip(
        *,
        db: Session = Depends(get_db),
        trip_id: int,
        current_user: schemas.UserResponse = Depends(get_current_user)
):
    trip = crud.trip.get(db, id=trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    #  只有trip的创建者才能删除trip
    if trip.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    trip = crud.trip.remove(db, id=trip_id)
    return trip


# 获取trip的详细信息
@router.get("/{trip_id}", response_model=schemas.TripResponse)
def get_trip(
        *,
        db: Session = Depends(get_db),
        trip_id: int,
        current_user: schemas.UserResponse = Depends(get_current_user)
):
    trip = crud.trip.get(db, id=trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    #   只有trip的创建者才能获取trip的详细信息
    if trip.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return trip

# 获取我所参与的所有trip
