from fastapi import Request, Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.model import Token, User
from auth.method import get_current_active_user, create_access_token, authenticate_user, get_password_hash
from datetime import timedelta
from constant import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/signup")
async def signup(request: Request, form_data: OAuth2PasswordRequestForm = Depends() ):
    if request.app.db.Users.find_one({"username": form_data.username}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user exist")

    user = {
        "username": form_data.username,
        "hashed_password": str(get_password_hash(form_data.password)),
    }
    result = request.app.db.users.insert_one(user)
    user["id"] = str(result.inserted_id)
    del user["_id"]

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"],"id":user["id"]}, expires_delta=access_token_expires
    )
    user['access_token'] = access_token

    return user

@router.post("/jwt/token", response_model=Token)# 1
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(request.app.db.Users, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)#獲取token過期時間
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/jwt/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# @router.post("jwt/signout")
# async def signout():
