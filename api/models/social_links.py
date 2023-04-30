from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from api.database import Base


class SocialLink(Base):
    __tablename__ = "social_links"

    id = Column(Integer, primary_key=True, index=True)
    artist_id = mapped_column(ForeignKey("artists.id"))
    artist = relationship("Artist", back_populates="social_links", lazy="joined")
    social_media_id = mapped_column(ForeignKey("social_media.id"))
    social_media = relationship("SocialMedia", lazy="joined")
    username = Column(String, nullable=False)

    @hybrid_property
    def output(self):
        return {
            "service": f"{self.social_media.name}",
            "url": self.social_media.url.format(self.username),
            "id": self.id,
        }
