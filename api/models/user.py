from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from api.database import Base


class User(Base):
  __tablename__ = "users"

  id =              Column(Integer, primary_key = True, index = True)
  name =            Column(String, unique = True, index = True, nullable = False)
  email =           Column(String, unique = True, index = True, nullable = False)
  password =        Column(String, nullable = False)
  sudo =            Column(Boolean, nullable = False, default = False)
  artist =          relationship("Artist", back_populates="user")