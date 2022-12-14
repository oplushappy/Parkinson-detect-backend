from typing import Union
from bson import ObjectId
from pydantic import BaseModel

class Token(BaseModel):#返回給用戶token
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class User(BaseModel):
    uid: str
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    real_name: str
    gender: str
    age: int = Field(..., gt=0, lt=100)


class UserInDB(User):
    hashed_password: str