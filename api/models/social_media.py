from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.database import Base


class SocialMedia(Base):
    __tablename__ = "social_media"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    social_link = relationship(
        "SocialLink", back_populates="social_media", lazy="joined"
    )
