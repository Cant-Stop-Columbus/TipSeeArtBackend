from fastapi import Depends, Response, status
from api import app
from sqlalchemy.orm import Session
from api.auth.auth_bearer import JWTBearer
from api.database import get_db
from api.schemas import ArtistSchema, ArtistRegister
from api.models import Artist, User

@app.get("/artists", response_model=list[ArtistSchema])
def artist_index(db: Session = Depends(get_db)):
    return db.query(Artist).all()

@app.get("/artists/{name}", response_model=ArtistSchema)
def get_artist(name : str , db: Session = Depends(get_db)):
    user = db.query(User).filter_by(name = name).first()
    


@app.post("/artists/create", status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
def create_artist(artist: ArtistRegister ):
    pass