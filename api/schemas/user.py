from typing import Optional
from pydantic import BaseModel, EmailStr


class UserSafe(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserIsSudo(UserSafe):
    sudo: bool


class UserRegister(UserSafe):
    email: EmailStr
    password: str
