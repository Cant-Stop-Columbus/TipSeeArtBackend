from datetime import timedelta
from typing import Annotated
import bcrypt
from api import SALT, app
from sqlalchemy import func
from sqlalchemy.orm import Session
from api.database import get_db
from fastapi import Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from api.schemas import UserRegister
from api.models import User
from api.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    Token,
)


@app.post("/user/create", status_code=status.HTTP_201_CREATED, response_model=Token)
async def create_user(user: UserRegister, db: Session = Depends(get_db)):
    try:
        user_data = {**user.dict()}
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


# @app.post("/user/login")
# async def login_user(
#     user: UserLogin, response: Response, db: Session = Depends(get_db)
# ):
#     try:
#         db_user = (
#             db.query(User)
#             .where(func.lower(User.email) == func.lower(user.email))
#             .first()
#         )
#         if db_user and bcrypt.checkpw(
#             user.password.encode(), db_user.password.encode()
#         ):
#             return {"authorization": signJWT(user.email), "status": "Success"}
#     except Exception as e:
#         raise HTTPException(401, detail=str(e))
#     raise HTTPException(401, detail="Invalid email or password")


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
