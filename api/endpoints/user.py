from datetime import timedelta
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import schemas
import models
import crud
from api import deps
from core import security
from core.security import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


# 用户注册
@router.post("/register", response_model=schemas.UserResponse)
async def register(
        *,
        db: Session = Depends(deps.get_db),
        user_in: schemas.UserCreate,
):
    # 检查用户名是否已存在
    if crud.user.get_by_username(db, username=user_in.username):
        raise HTTPException(status_code=400, detail="Username already registered")

    # 创建新用户
    user = crud.user.create(db, obj_in=user_in)
    return user


#  用户登录，返回token
@router.post("/login", response_model=schemas.Token)
async def login_access_token(
        db: Session = Depends(deps.get_db),
        user_credentials: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    # 检查用户名和密码是否匹配
    user = crud.user.authenticate(
        db, username=user_credentials.username, password=user_credentials.password
    )
    if not user:
        raise HTTPException(status_code=403, detail="Invalid username or password")

    # 生成JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# 获取所有用户
@router.get("/users/", response_model=List[schemas.UserResponse])
async def read_users(
        *,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_user),
        ) -> Any:
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users
