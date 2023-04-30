from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from api.database import Base


class PaymentUrl(Base):
    __tablename__ = "payment_urls"

    id = Column(Integer, primary_key=True, index=True)
    artist_id = mapped_column(ForeignKey("artists.id"))
    artist = relationship("Artist", back_populates="payment_urls", lazy="joined")
    payment_provider_id = mapped_column(ForeignKey("payment_providers.id"))
    payment_provider = relationship("PaymentProvider", lazy="joined")
    username = Column(String, nullable=False)

    @hybrid_property
    def output(self):
        return {
            "service": f"{self.payment_provider.name}",
            "url": self.payment_provider.url.format(self.username),
        }
