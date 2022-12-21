from datetime import datetime, timedelta
import re
from typing import Optional
from fastapi import Depends, HTTPException, status
from constant import SECRET_KEY, ALGORITHM, pwd_context, oauth2_scheme
from jose import jwt, JWTError
from auth.model import UserInDB, User, TokenData
from database import MONGODB
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

def get_password_hash(password):  # used in signup
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()  #do a copy

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=240)
    to_encode.update({"exp": expire})  #make sure have a time expire(year mon day hr:min)
    
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# used in signin
def authenticate_user(user_db_collection, username: str, password: str):
    if re.search(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', username):
        username = username.lower()
        user = get_email(user_db_collection, email=username)
        if user is None:
            return False
    else:
        user = get_user(user_db_collection, username=username)
        if user is None:
            return False
    if not verify_password(password, user.hashed_password):  #if exist check whether be smae with hash_password
        return False
    return user


def get_email(user_db_collection, email: str):
    user = user_db_collection.find_one({"email": email})
    if user:
        user_dict = user
        user_dict["uid"] = str(user["_id"])
        return UserInDB(**user_dict)#使參數變為dict
    return None

def get_user(user_db_collection, username: str):
    user = user_db_collection.find_one({"username": username})
    if user:
        user_dict = user
        user_dict["uid"] = str(user["_id"])
        return UserInDB(**user_dict)#使參數變為dict
                # also return hash password to let use verify_password function
    return None

# use user provide plain password to verify
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)





# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"authorization": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(MONGODB.Users, token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user

# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


