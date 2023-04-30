from datetime import timedelta
from api import app
from sqlalchemy.orm import Session
from api.database import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.schemas import UserRegister, UserArtist
from api.models import User
from api.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    Token,
)


@app.post("/user/create", status_code=status.HTTP_201_CREATED, response_model=Token)
async def create_user(user: UserRegister, db: Session = Depends(get_db)):
    try:
        user_data = user.dict()
        user_data["password"] = get_password_hash(user_data["password"])
        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
    except Exception as e:
        raise HTTPException(400, detail=str(e))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    try:
        user = authenticate_user(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/me", response_model=UserArtist)
def get_me(user: User = Depends(get_current_user)):
    return user.artist_output
