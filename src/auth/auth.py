from fastapi import Request, Depends, APIRouter, HTTPException, status, Form
from bson import ObjectId
from fastapi.security import OAuth2PasswordRequestForm
from auth.model import Token, User
from auth.method import  create_access_token, authenticate_user, get_password_hash #get_current_active_user,
from datetime import timedelta, datetime
from constant import ACCESS_TOKEN_EXPIRE_MINUTES
from tool.emailer import sendtoemail 
from subject.method import form_change_to_json


router = APIRouter()


@router.post("/signup",status_code=201)
async def signup(request: Request, username: str = Form(), password: str = Form(), email: str = Form() ):
    if request.app.db.users.find_one({"username": username}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user exist")
    if email is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"require email field")
    user = {
        "username": username,
        "hashed_password": str(get_password_hash(password)),
        "email": email,
        "verify": False
    }
    result = request.app.db.users.insert_one(user)
    user["id"] = str(result.inserted_id)  #make sure that only one id
    del user["_id"]
    verify_token = sendtoemail(email, user["id"])
    if(verify_token):
        emial_verify = request.app.db.email_verify.insert_one({
            "email_token": verify_token,
            "expire": datetime.utcnow() + timedelta(minutes=10)
        })

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "id":user["id"], "verify":user["verify"]}, expires_delta=access_token_expires
    )
    user['access_token'] = access_token
    return user

@router.get("/verify/")
def verify_email(request:Request, verify_token: str, user_id: str):
    res = request.app.db.email_verify.find_one({"email_token": verify_token})
    if res is None:
        raise HTTPException(status_code=404)
    if(datetime.utcnow() > res["expire"]):
        raise HTTPException(status_code=498, detail="expired")
    user = request.app.db.users.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": {"verify":True}},
        upsert=True
    )
    print(user.get("username"))
    user["id"] = str(user["_id"])
    del user["_id"]
    # email_verify = request.app.db.email_verify.find_one_and_delete({"email_token":verify_token})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "id":user["id"], "verify":user["verify"]}, expires_delta=access_token_expires
    )
    user['access_token'] = access_token 
    return user

@router.post("/jwt/token", response_model=Token)# 1
async def signin(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(request.app.db.users, form_data.username, form_data.password)  #verify password in this phase
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"authorization": "Bearer"},
        )
    if user.verify == False:
        sendtoemail(user.email)
        raise HTTPException(status_code=401,detail="email send")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)#獲取token過期時間
    access_token = create_access_token(
        data={"sub": user.username, "id":user.uid, "verify":user.verify}, expires_delta=access_token_expires
    )  #sign in will create a new token

    return {"access_token": access_token, "token_type": "Bearer"}  #return access token to let frontend put access token to header bearer

@router.post("/signout")
async def signout():
    return

@router.post("chanfe/password")
async def changepassword():
    return

@router.post("send/verift_number")
async def send_verify_number():
    return

# @router.get("/jwt/users/me/", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user

# @router.post("jwt/signout")
# async def signout():
