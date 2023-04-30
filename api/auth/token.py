#! NB: Don't mess with this file unless you know what you're doing!
#!     (This is part of the code that handles user login and persistence;
#!      if you break this, no one will be able to login and change things)

from pydantic import BaseModel
from typing import Union


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
