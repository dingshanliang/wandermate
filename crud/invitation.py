from fastapi.encoders import jsonable_encoder

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


invitation = CRUDInvitation(Invitation)
