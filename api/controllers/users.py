import bcrypt
from api import SALT, app
from sqlalchemy import func
from sqlalchemy.orm import Session
from api.auth.auth_bearer import JWTBearer
from api.auth.auth_handler import signJWT
from api.database import get_db
from fastapi import Depends, HTTPException, Response, status
from api.schemas import UserRegister, UserLogin
from api.models import  User

@app.post('/user/create', status_code=status.HTTP_201_CREATED)
async def create_user(user: UserRegister, response: Response, db: Session = Depends(get_db)):
  try:
    user_data = {**user.dict()}
    user_data['password'] = bcrypt.hashpw(user_data['password'].encode(),SALT).decode("UTF-8")
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
  except Exception as e:
    raise HTTPException(400, detail = str(e))
  return {
        "authorization": signJWT(user.email),
        "status": "Success"
        }

@app.post("/user/login")
async def login_user(user: UserLogin, response: Response, db: Session = Depends(get_db)):
  try:
    db_user = db.query(User).where(func.lower(User.email) == func.lower(user.email)).first()
    if db_user and bcrypt.checkpw(user.password.encode(), db_user.password.encode()):
      return {
        "authorization": signJWT(user.email),
        "status": "Success"
        }
  except Exception as e:
    raise HTTPException(401, detail= str(e))
  raise HTTPException(401, detail= "Invalid email or password")