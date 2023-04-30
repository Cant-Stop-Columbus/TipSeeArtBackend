from fastapi import Depends, File, HTTPException, Response, status, UploadFile, Form
from api import app
from sqlalchemy.orm import Session
from api.database import get_db
from api.schemas import ArtistSchema
from api.models import (
    Artist,
    User,
    PaymentProvider,
    PaymentUrl,
    SocialMedia,
    SocialLink,
)
from api.schemas import ArtistBase, PaymentCreate, ArtistFull, SocialCreate
from typing import Optional
from api.utils.file_upload import upload_image
from api.auth import get_current_user


@app.get("/artists", response_model=list[ArtistSchema])
def artist_index(db: Session = Depends(get_db)):
    return db.query(Artist).all()


@app.get("/artists/{name}", response_model=ArtistFull)
def get_artist(name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=name).first()
    artist = None
    if user:
        artist = db.query(Artist).filter_by(user_id=user.id).first()
    if artist:
        return artist.full_output
    else:
        raise HTTPException(
            status_code=404, detail=f"Artist not found for user with name {name}"
        )


@app.post("/artists/create", status_code=status.HTTP_201_CREATED)
def create_artist(
    artist: ArtistBase,
    payment_urls: Optional[list[PaymentCreate]],
    social_links: Optional[list[SocialCreate]],
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    artist = artist.dict()
    existing_artist = db.query(Artist).filter_by(user_id=user.id).first()
    if existing_artist:
        raise HTTPException(400, "Artist already exists for this user")
    try:
        db_artist = Artist(**artist, user_id=user.id)
        db.add(db_artist)
        db.commit()
        db.refresh(db_artist)
        for payment in payment_urls:
            provider = (
                db.query(PaymentProvider).filter_by(name=payment.provider_name).first()
            )
            if not provider:
                provider = db.query(PaymentProvider).filter_by(name="other").first()
            db_url = PaymentUrl(
                artist_id=db_artist.id,
                payment_provider_id=provider.id,
                username=payment.username,
            )
            db.add(db_url)
        for social in social_links:
            media = db.query(SocialMedia).filter_by(name=social.social_name).first()
            if not media:
                media = db.query(SocialMedia).filter_by(name="other").first()
            db_url = SocialLink(
                artist_id=db_artist.id,
                social_media_id=media.id,
                username=payment.username,
            )
            db.add(db_url)
        db.commit()
        db.refresh(db_artist)
        return db_artist.full_output
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/artists/update", response_model=ArtistSchema)
def update_artist(
    updated_values: ArtistBase,
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
            url = upload_image(file, f"{user.username}_profile_pic.{t[1]}")
            artist.profile_pic_url = url
            db.commit()
            return artist
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=404, detail="No Artist found for this user")
