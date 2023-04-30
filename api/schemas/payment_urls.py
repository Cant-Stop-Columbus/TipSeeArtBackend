from pydantic import BaseModel


class PaymentSchema(BaseModel):
    service: str
    url: str
    id: int


class PaymentCreate(BaseModel):
    provider_name: str
    username: str

    class Config:
        orm_mode = True


class PaymentUpdate(PaymentCreate):
    id: int
