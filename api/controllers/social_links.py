from api import app
from fastapi import Depends, HTTPException
from api.database import get_db
from api.auth import get_current_user
from sqlalchemy.orm import Session
from api.models import User, Artist, SocialLink, SocialMedia

from api.schemas import SocialUpdate, SocialCreate


@app.post("/social/add")
async def add_payment_methods(
    social: SocialCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        artist = db.query(Artist).filter_by(user_id=user.id).first()
        if not artist:
            raise HTTPException(404, "Artist not found for this user")
        existing_socials = dict(
            list(
                map(
                    lambda x: (x.social_media.name, x.social_media.id),
                    artist.social_links,
                )
            )
        )
        if social.social_name == "other":
            db.add(
                SocialLink(
                    username=social.username,
                    social_media_id=1,
                    artist_id=artist.id,
                )
            )
        elif social.social_name not in existing_socials.keys():
            method = db.query(SocialMedia).filter_by(name=social.social_name).first()
            method_id = 1
            if method:
                method_id = method.id
            db.add(
                SocialLink(
                    username=social.username,
                    social_media_id=method_id,
                    artist_id=artist.id,
                )
            )
        else:
            raise HTTPException(400, f"Link for {social.social_name} already exists")
        db.commit()
        db.refresh(artist)
        return artist.full_output
    except Exception as e:
        raise HTTPException(500, str(e))


@app.patch("/social/update")
async def update_payment(
    updated: SocialUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        social_link = db.query(SocialLink).get(updated.id)
        if not social_link:
            raise HTTPException(404, f"Link {updated.id} not found")
        artist = db.query(Artist).filter_by(user_id=user.id).first()
        if not artist:
            raise HTTPException(404, "Artist not found for this user")
        social_link.username = updated.username
        db.commit()
        db.refresh(artist)
        return artist.full_output
    except Exception as e:
        raise HTTPException(500, str(e))


@app.delete("/social/delete")
async def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        social_link = db.query(SocialLink).get(payment_id)
        if not social_link:
            raise HTTPException(404, f"Link {payment_id} not found")
        artist = db.query(Artist).filter_by(user_id=user.id).first()
        if not artist:
            raise HTTPException(404, "Artist not found for this user")
        if social_link.artist_id == artist.id:
            db.delete(social_link)
            db.commit()
            db.refresh(artist)
            return artist.full_output
        else:
            raise HTTPException(
                401, "Only the owner of this payment_method is allowed to delete it"
            )
    except Exception as e:
        raise HTTPException(500, str(e))
