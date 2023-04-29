import os
import time
from typing import Dict
import jwt

def token_response(token: str):
  return {
    "access_token": token
  }

def signJWT(user_id: str) -> Dict[str, str]:
  payload = {
    "user_id": user_id,
    "expires": time.time() + 3600
  }
  token = jwt.encode(payload, os.environ["JWT_SECRET"], algorithm=os.environ["JWT_ALGORITHM"])

  return token_response(token)

def decodeJWT(token: str) -> dict:
  try:
    decoded_token = jwt.decode(token, os.environ["JWT_SECRET"], algorithms=[os.environ["JWT_ALGORITHM"]])
    return decoded_token if decoded_token["expires"] >= time.time() else None
  except:
    return {}