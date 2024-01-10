import binascii
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from geoalchemy2.shape import to_shape

import crud
import models
import schemas
from api import deps

router = APIRouter()


# 创建活动
@router.post("/{trip_id}", response_model=schemas.ActivityResponse)
def create_activity(
        *,
        db: Session = Depends(deps.get_db),
        trip_id: int,
        activity_in: schemas.ActivityCreate,
        current_user: models.User = Depends(deps.get_current_user)
):
    """
    返回：
    {
  "id": 21,
  "title": "string",
  "start_time": "2024-01-10T08:57:34.440000",
  "coordinates": "POINT (0 0)",
  "creator_id": 1,
  "trip_id": 7,
  "description": "string",
  "end_time": "2024-01-10T08:57:34.440000"
}
    """
    # 先判断用户是否是这个trip的创建者或者被邀请者，通过查邀请表实现，邀请表中的trip_id等于trip_id的情况下，
    # 查看current_user.id 是否等于inviter_id或者invitee_id
    # 或者查看trip表，看此trip的creator_id是否等于current_user.id

    trip = crud.trip.get(db, id=trip_id)
    invitation = db.query(models.Invitation).filter(
        models.Invitation.trip_id == trip_id,
        (models.Invitation.inviter_id == current_user.id) |
        (models.Invitation.invitee_id == current_user.id)
    ).first()
    if not invitation and trip.creator_id is not current_user.id:  # 用户既不在此条trip记录的邀请表里，也不是trip的创建者，则无权创建活动
        raise HTTPException(status_code=403, detail="无权限创建活动")

    # 创建活动
    activity = crud.activity.create_by_trip_and_user(db, activity_in=activity_in, creator_id=current_user.id,
                                                     trip_id=trip_id)

    # 将数据库中的坐标由WKBELement转为WKT
    activity.coordinates = to_shape(activity.coordinates).wkt

    return activity


# 更新活动
@router.put("/{activity_id}", response_model=schemas.ActivityResponse)
def update_activity(
        *,
        db: Session = Depends(deps.get_db),
        activity_id: int,
        activity_in: schemas.ActivityUpdate,
        current_user: models.User = Depends(deps.get_current_user),
):
    # 查询活动
    activity = crud.activity.get(db, id=activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="活动不存在")

    activity = crud.activity.update(db, db_activity=activity, activity_in=activity_in)

    # 返回之前，将数据库中的坐标由WKBELement转为WKT，否则无法序列化
    activity.coordinates = to_shape(activity.coordinates).wkt

    return activity


# 根据 id 查询活动
@router.get("/{activity_id}", response_model=schemas.ActivityResponse)
def read_activity(
        *,
        db: Session = Depends(deps.get_db),
        activity_id: int,
        current_user: models.User = Depends(deps.get_current_user),
):
    activity = crud.activity.get(db, id=activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="活动不存在")

    # 返回之前，将数据库中的坐标由WKBELement转为WKT，否则无法序列化
    activity.coordinates = to_shape(activity.coordinates).wkt

    return activity


# 查询所有活动
@router.get("/", response_model=List[schemas.ActivityResponse])
def read_activities(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
):
    activities = crud.activity.get_multi(db)

    # 返回之前，将数据库中的坐标由WKBELement转为WKT，否则无法序列化
    for activity in activities:
        activity.coordinates = to_shape(activity.coordinates).wkt

    return activities


# 删除活动
@router.delete("/{activity_id}", response_model=schemas.ActivityResponse)
def delete_activity(
        *,
        db: Session = Depends(deps.get_db),
        activity_id: int,
        current_user: models.User = Depends(deps.get_current_user),
):
    activity = crud.activity.get(db, id=activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="活动不存在")

    activity = crud.activity.remove(db, id=activity_id)

    # 返回之前，将数据库中的坐标由WKBELement转为WKT，否则无法序列化
    activity.coordinates = to_shape(activity.coordinates).wkt

    return activity
