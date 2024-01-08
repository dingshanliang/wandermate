from typing import Generator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

import crud
import models
import schemas
from core.security import SECRET_KEY, ALGORITHM
from db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# 通过token 获取当前用户
def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    print(f"Token: {token}")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
    # except (jwt.JWTError, ValidationError):
    except Exception as e:
        print(f"Exception details: {e}")
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
