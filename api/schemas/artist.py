from pydantic import BaseModel
from typing import Optional

from api.schemas.user import UserSafe


class ArtistUpdate(BaseModel):
    description: str

    class Config:
        orm_mode = True


class ArtistRegister(ArtistUpdate):
    user_id: int


class ArtistForUser(ArtistUpdate):
    profile_pic_url: Optional[str]


class ArtistWithId(ArtistUpdate):
    id: int


class ArtistSchema(ArtistUpdate):
    user: UserSafe
    profile_pic_url: Optional[str]
