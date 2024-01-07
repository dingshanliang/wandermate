from fastapi import APIRouter

from .endpoints import user

router = APIRouter()

# 添加路由
router.include_router(user.router, tags=["user"])
