from typing import Optional
from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserSafe(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserIsSudo(UserSafe):
    sudo: bool


class UserRegister(UserSafe):
    password: str
