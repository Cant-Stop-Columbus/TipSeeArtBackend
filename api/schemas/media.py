from pydantic import BaseModel


class MediaSchema(BaseModel):
    media_type: str
    url: str
