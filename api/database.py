#! NB: Don't mess with this file unless you know what you're doing!

import os
from sqlalchemy import Column, ForeignKey, Integer, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.utils.sqlify import sqlify

engine = create_engine(sqlify())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
