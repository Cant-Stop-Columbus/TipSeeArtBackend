from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from api.database import Base


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    media_type = Column(String, nullable=False)
    artist_id = mapped_column(ForeignKey("artists.id"))
    artist = relationship("Artist", back_populates="media", lazy="joined")
