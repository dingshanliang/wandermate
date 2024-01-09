from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from api import deps
from api.deps import get_current_user

router = APIRouter()


# 针对某个trip邀请朋友参与
@router.post("/", response_model=schemas.InvitationResponse)
def create_invitation(
        *,
        db: Session = Depends(deps.get_db),
        invitation_in: schemas.InvitationCreate,
        current_user: schemas.UserResponse = Depends(get_current_user)
):
    # 首先判断是否已经存在邀请
    existing_invitation = (
        db.query(models.Invitation)
            .filter_by(
            trip_id=invitation_in.trip_id,
            inviter_id=current_user.id,
            invitee_id=invitation_in.invitee_id
        )).first()

    if existing_invitation:
        raise HTTPException(status_code=400, detail="Invitation already exists")

    #  创建邀请
    invitation = crud.invitation.create_with_user_id(db, obj_in=invitation_in, inviter_id=current_user.id)
    return invitation


# 更新邀请,应该只针对某条邀请更新状态，而且只能是被邀请人来更新，是否接受
@router.put("/{invitation_id}", response_model=schemas.InvitationResponse)
def update_invitation(
        *,
        db: Session = Depends(deps.get_db),
        invitation_id: int,
        update_status: schemas.InvitationStatus,
        current_user: schemas.UserResponse = Depends(get_current_user)
):
    invitation = crud.invitation.get(db=db, id=invitation_id)
    #  判断邀请是否存在
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")

    # 判断邀请是否属于当前用户
    if invitation.invitee_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this invitation")

    # 更新邀请状态
    invitation_updated = crud.invitation.update_with_invitation_id(db,db_obj=invitation, update_status=update_status)
    return invitation_updated


# 删除邀请,本质其实就是将某个人从该trip中踢出去
@router.delete("/{invitation_id}", response_model=schemas.InvitationResponse)
def delete_invitation(
        *,
        db: Session = Depends(deps.get_db),
        invitation_id: int,
        current_user: schemas.UserResponse = Depends(get_current_user)
):
    invitation = crud.invitation.get(db=db, id=invitation_id)
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")

    # 只有邀请人才能删除邀请
    if invitation.inviter_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this invitation")

    invitation = crud.invitation.remove(db=db, id=invitation_id)
    return invitation


# 获取被邀请列表
@router.get("/", response_model=List[schemas.InvitationResponse])
def get_invitations(
        *,
        db: Session = Depends(deps.get_db),
        current_user: schemas.UserResponse = Depends(get_current_user),
):
    invitations = crud.invitation.get_by_user_id(db=db, user_id=current_user.id)
    return invitations


