from datetime import timedelta

from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from auth.login import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#返回哈希密碼
def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/signup")
async def signup(request: Request, form_data: OAuth2PasswordRequestForm = Depends() ):
    if request.app.db.Users.find_one({"username": form_data.username}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user exist")

    user = {
        "username": form_data.username,
        "password": str(get_password_hash(form_data.password))
    }
    result = request.app.db.Users.insert_one(user)
    user["id"] = str(result.inserted_id)
    del user["_id"]

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    user['access_token'] = access_token

    return user
