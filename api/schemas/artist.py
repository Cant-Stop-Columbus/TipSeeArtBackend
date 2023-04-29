from pydantic import BaseModel
from .user import UserSafe
from typing import Optional

class ArtistRegister(BaseModel):
    description: str
    profile_pic_url: Optional[str]
    user_id: int

    class Config:
        orm_mode = True

class ArtistSchema(BaseModel):
    user: UserSafe
    description: str
    profile_pic_url: Optional[str]


    class Config:
        orm_mode = True