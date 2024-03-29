from fastapi import APIRouter

from .endpoints import user
from .endpoints import trips
from .endpoints import invitations

router = APIRouter()

# 添加路由
router.include_router(user.router, tags=["user"])
router.include_router(trips.router, prefix="/trips", tags=["trips"])
router.include_router(invitations.router, prefix="/invitations", tags=["invitations"])
