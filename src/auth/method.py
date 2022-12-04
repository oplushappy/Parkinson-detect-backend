from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from constant import SECRET_KEY, ALGORITHM, pwd_context, oauth2_scheme
from jose import jwt, JWTError
from auth.model import UserInDB, User, TokenData
from database import MONGODB

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()#copy一份，進行編碼

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#確認使用者
def get_user(user_db_collection, username: str):
    # if username in user_db:
    user = user_db_collection.find_one({"username": username})
    if user:
        user_dict = user
        return UserInDB(**user_dict)#使參數變為dict

#驗整密碼
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#驗證使用者
def authenticate_user(user_db_collection, username: str, password: str):
    user = get_user(user_db_collection, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_password_hash(password):
    return pwd_context.hash(password)

#驗整密碼
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(MONGODB.Users, token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


