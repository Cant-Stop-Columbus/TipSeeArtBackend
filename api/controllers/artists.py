from fastapi import Depends, File, HTTPException, Response, status, UploadFile, Form
from api import app
from sqlalchemy.orm import Session, joinedload
from api.database import get_db
from api.schemas import ArtistSchema, ArtistRegister
from api.models import Artist, User
from api.schemas import ArtistUpdate, ArtistWithId
from api.utils.file_upload import upload_image
from api.auth import get_current_user


@app.get("/artists", response_model=list[ArtistSchema])
def artist_index(db: Session = Depends(get_db)):
    return db.query(Artist).all()


@app.get("/artists/{name}", response_model=ArtistSchema)
def get_artist(name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=name).first()
    artist = None
    if user:
        artist = db.query(Artist).filter_by(user_id=user.id).first()
    if artist:
        return artist
    else:
        raise HTTPException(
            status_code=404, detail=f"Artist not found for user with name {name}"
        )


@app.post(
    "/artists/create", status_code=status.HTTP_201_CREATED, response_model=ArtistWithId
)
def create_artist(
    artist: ArtistUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    artist = artist.dict()
    existing_artist = db.query(Artist).filter_by(user_id=user.id).first()
    if existing_artist:
        return {"Error": "Artist already exists for this user"}
    try:
        db_artist = Artist(**artist, user_id=user.id)
        db.add(db_artist)
        db.commit()
        return db_artist
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/artists/update", response_model=ArtistSchema)
def update_artist(
    updated_values: ArtistUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not user.artist:
        raise HTTPException(404, "Artist not found for this user")
    artist = db.query(Artist).filter_by(user_id=user.id).first()
    for k, v in updated_values.dict().items():
        setattr(artist, k, v)
    return artist


@app.put("/artists/profile_pic", response_model=ArtistSchema)
def update_profile_pic(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
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
    artist = db.query(Artist).filter_by(user_id=user.id).first()
    if artist:
        try:
            url = upload_image(file, f"{user.username}_profile_pic")
            artist.profile_pic_url = url
            db.commit()
            return artist
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=404, detail="No Artist found for this user")
