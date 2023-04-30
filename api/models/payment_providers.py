from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.database import Base


class PaymentProider(Base):
    __tablename__ = "payment_providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    artist = relationship(
        "PaymentUrl", back_populates="payment_providers", lazy="joined"
    )
