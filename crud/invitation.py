from fastapi.encoders import jsonable_encoder

import schemas
from crud.base import CRUDBase
from models import Invitation
from schemas import InvitationCreate, InvitationUpdate


class CRUDInvitation(CRUDBase[Invitation, InvitationCreate, InvitationUpdate]):
    # 根据用户id创建邀请
    def create_with_user_id(self, db, *, obj_in: InvitationCreate, inviter_id: int) -> Invitation:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, inviter_id=inviter_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # 根据用户id获取所有邀请（被邀请）
    def get_by_user_id(self, db, *, user_id: int) -> Invitation:
        return db.query(self.model).filter(self.model.invitee_id == user_id).all()

    # 根据邀请id更新邀请状态
    def update_with_invitation_id(self, db, *, db_obj: Invitation, update_status):
        setattr(db_obj, 'status', update_status)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


invitation = CRUDInvitation(Invitation)
