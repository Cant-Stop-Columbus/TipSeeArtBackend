from api import app
from fastapi import Depends, HTTPException
from api.database import get_db
from api.auth import get_current_user
from sqlalchemy.orm import Session
from api.models import User, Artist, PaymentUrl, PaymentProvider

from api.schemas import PaymentUpdate, PaymentCreate


@app.post("/payments/add")
async def add_payment_methods(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        artist = db.query(Artist).filter_by(user_id=user.id).first()
        if not artist:
            raise HTTPException(404, "Artist not found for this user")
        existing_payments = dict(
            list(
                map(
                    lambda x: (x.payment_provider.name, x.payment_provider.id),
                    artist.payment_urls,
                )
            )
        )
        if payment.provider_name == "other":
            db.add(
                PaymentUrl(
                    username=payment.username,
                    payment_provider_id=1,
                    artist_id=artist.id,
                )
            )
        elif payment.provider_name not in existing_payments.keys():
            method = (
                db.query(PaymentProvider).filter_by(name=payment.provider_name).first()
            )
            method_id = 1
            if method:
                method_id = method.id
            db.add(
                PaymentUrl(
                    username=payment.username,
                    payment_provider_id=method_id,
                    artist_id=artist.id,
                )
            )
        else:
            raise HTTPException(
                400, f"Payment method from {payment.provider_name} already exists"
            )
        db.commit()
        db.refresh(artist)
        return artist.full_output
    except Exception as e:
        raise HTTPException(500, str(e))


@app.patch("/payments/update")
async def update_payment(
    updated: PaymentUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        payment_url = db.query(PaymentUrl).get(updated.id)
        if not payment_url:
            raise HTTPException(404, f"Payment {updated.id} not found")
        artist = db.query(Artist).filter_by(user_id=user.id).first()
        if not artist:
            raise HTTPException(404, "Artist not found for this user")
        payment_url.username = updated.username
        db.commit()
        db.refresh(artist)
        return artist.full_output
    except Exception as e:
        raise HTTPException(500, str(e))


@app.delete("/payments/delete")
async def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        payment_url = db.query(PaymentUrl).get(payment_id)
        if not payment_url:
            raise HTTPException(404, f"Payment {payment_id} not found")
        artist = db.query(Artist).filter_by(user_id=user.id).first()
        if not artist:
            raise HTTPException(404, "Artist not found for this user")
        if payment_url.artist_id == artist.id:
            db.delete(payment_url)
            db.commit()
            db.refresh(artist)
            return artist.full_output
        else:
            raise HTTPException(
                401, "Only the owner of this payment_method is allowed to delete it"
            )
    except Exception as e:
        raise HTTPException(500, str(e))
