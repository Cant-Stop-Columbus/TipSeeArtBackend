from pydantic import BaseModel
from typing import Optional
from api.schemas.media import MediaSchema

from api.schemas.user import UserSafe
from api.schemas.payment_urls import PaymentSchema, PaymentCreate


class ArtistBase(BaseModel):
    description: str

    class Config:
        orm_mode = True


class ArtistRegister(ArtistBase):
    user_id: int


class ArtistForUser(ArtistBase):
    profile_pic_url: Optional[str]


class ArtistWithId(ArtistBase):
    id: int


class ArtistSchema(ArtistBase):
    user: UserSafe
    profile_pic_url: Optional[str]


class ArtistFull(ArtistSchema):
    media: list[MediaSchema]
    payment_urls: list[PaymentSchema]


class ArtistUpdate(ArtistBase):
    payment_providers: list[PaymentCreate]
