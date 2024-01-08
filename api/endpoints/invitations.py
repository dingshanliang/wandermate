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


# 更新邀请
@router.put("/{invitation_id}", response_model=schemas.InvitationResponse)
def update_invitation(
        *,
        db: Session = Depends(deps.get_db),
        invitation_id: int,
        invitation_in: schemas.InvitationUpdate,
        current_user: schemas.UserResponse = Depends(get_current_user)
):
    invitation = crud.invitation.get(db=db, id=invitation_id)
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")

    invitation = crud.invitation.update(db=db, db_obj=invitation, obj_in=invitation_in)
    return invitation


# 删除邀请
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

    invitation = crud.invitation.remove(db=db, id=invitation_id)
    return invitation
