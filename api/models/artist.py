from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from api.database import Base

class Artist(Base):
  __tablename__ = "artists"

  id =                                Column(Integer, primary_key = True, index = True)
  description =                       Column(String, nullable=False, default="")
  profile_pic_url =                   Column(String)
  user_id =                           mapped_column(ForeignKey("users.id"))
  user =                              relationship("User")
