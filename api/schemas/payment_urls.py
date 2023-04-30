from pydantic import BaseModel


class PaymentSchema(BaseModel):
    service: str
    url: str


class PaymentUpdate(BaseModel):
    provider_name: str
    username: str

    class Config:
        orm_mode = True
