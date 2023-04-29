from fastapi import Depends, File, HTTPException, Response, status, UploadFile, Form
from api import app
from sqlalchemy.orm import Session
from api.database import get_db
from api.schemas import ArtistSchema, ArtistRegister
from api.models import Artist, User
from api.utils.file_upload import upload_image


@app.get("/artists", response_model=list[ArtistSchema])
def artist_index(db: Session = Depends(get_db)):
    return db.query(Artist).all()


@app.get("/artists/{name}", response_model=ArtistSchema)
def get_artist(name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(name=name).first()
    artist = None
    if user:
        artist = db.query(Artist).filter_by(user_id=user.id).first()
    if artist:
        return artist
    else:
        raise HTTPException(
            status_code=404, detail=f"Artist not found for user with name {name}"
        )


@app.post("/artists/create", status_code=status.HTTP_201_CREATED)
def create_artist(artist: ArtistRegister, db: Session = Depends(get_db)):
    artist = artist.dict()
    existing_artist = db.query(Artist).filter_by(user_id=artist["user_id"]).first()
    if existing_artist:
        return {"Error": f"Artist already exists for user with id {artist['user_id']}"}
    try:
        db_artist = Artist(**artist)
        db.add(db_artist)
        db.commit()
        return {**artist, "id": db_artist.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# @app.patch("/artists/{id}/update")


@app.put("/artists/profile_pic")
def update_profile_pic(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    t = file.content_type.split("/")
    if file.size > 5000000:
        raise HTTPException(
            status_code=400, detail="Profile pictures must be 5MB or less "
        )
    if t[0] != "image":
        raise HTTPException(
            status_code=400,
            detail="Only images can be uploaded as a profile picture",
        )
    artist = db.query(Artist).filter_by(user_id=user_id).first()
    if artist:
        try:
            url = upload_image(file, f"{user_id}_profile_pic")
            artist.profile_pic_url = url
            db.commit()
            return artist
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(
            status_code=404, detail=f"No Artist found for user with id of {user_id}"
        )
