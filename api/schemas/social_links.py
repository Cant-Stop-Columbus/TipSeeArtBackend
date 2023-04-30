from pydantic import BaseModel


class SocialSchema(BaseModel):
    service: str
    url: str
    id: int


class SocialCreate(BaseModel):
    social_name: str
    username: str

    class Config:
        orm_mode = True


class SocialUpdate(SocialCreate):
    id: int
