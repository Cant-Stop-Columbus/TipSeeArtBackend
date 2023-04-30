from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from api.database import Base
from sqlalchemy.ext.hybrid import hybrid_property


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    sudo = Column(Boolean, nullable=False, default=False)
    artist = relationship("Artist", back_populates="user", lazy="joined")

    @hybrid_property
    def artist_output(self):
        artist = self.artist
        if artist:
            artist = {
                "profile_pic_url": artist[0].profile_pic_url or None,
                "description": artist[0].description or None,
            }
        else:
            artist = {"profile_pic_url": None, "description": ""}
        return {
            "username": self.username,
            "email": self.email,
            "artist": artist,
        }
