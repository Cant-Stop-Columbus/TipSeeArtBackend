from pydantic import BaseModel
from .user import UserSafe
from typing import Optional


class ArtistUpdate(BaseModel):
    description: str

    class Config:
        orm_mode = True


class ArtistRegister(ArtistUpdate):
    user_id: int


class ArtistSchema(ArtistUpdate):
    user: UserSafe
    profile_pic_url: Optional[str]
