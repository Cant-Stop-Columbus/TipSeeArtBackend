from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from api.database import Base
from sqlalchemy.ext.hybrid import hybrid_property


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False, default="")
    profile_pic_url = Column(String)
    user_id = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="artist", lazy="joined")
    payment_urls = relationship("PaymentUrl", lazy="joined")
    media = relationship("Media")

    @hybrid_property
    def full_output(self):
        pay_urls = list(map(lambda x: x.output, self.payment_urls))
        return {
            "description": self.description,
            "user": {"username": self.user.username, "email": self.user.email},
            "payment_urls": pay_urls,
            "media": self.media,
            "profile_pic_url": self.profile_pic_url,
        }
