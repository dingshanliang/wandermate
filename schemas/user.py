from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    avatar: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    hashed_password: str


class UserResponse(UserInDBBase):
    pass
