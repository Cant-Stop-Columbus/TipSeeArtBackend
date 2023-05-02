import string
from fastapi import Depends, File, HTTPException, UploadFile
from api import app
from api.database import get_db
from api.auth import get_current_user
from sqlalchemy.orm import Session
from api.models import User, Artist, Media
from api.utils.file_upload import upload_image
from random import choices


@app.post("/media/upload")
async def media_upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    t = file.content_type.split("/")
    if file.size > 15000000:
        raise HTTPException(
            status_code=400, detail="Media uploads must be 15MB or less "
        )
    if t[0] not in ["image", "video"]:
        raise HTTPException(
            status_code=400,
            detail="Only images and videos can be uploaded as media",
        )
    artist = db.query(Artist).filter_by(user_id=user.id).first()
    if artist:
        try:
            url = upload_image(
                file,
                f"{''.join(choices(string.ascii_uppercase + string.digits, k=16))}.{t[1]}",
            )
            media = Media(url=url, media_type=t[0], artist_id=artist.id)
            db.add(media)
            db.commit()
            db.refresh(artist)
            return artist.full_output
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=404, detail="No Artist found for this user")
