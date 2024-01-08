from fastapi import APIRouter

from .endpoints import user
from .endpoints import trips

router = APIRouter()

# 添加路由
router.include_router(user.router, tags=["user"])
router.include_router(trips.router, tags=["trips"])
