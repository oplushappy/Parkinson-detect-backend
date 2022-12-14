from fastapi import FastAPI
from database import MONGODB
from subject.subject import router as subject_router
from result import router as result_router
from video import router as video_router
from auth.auth import router as auth_router

from fastapi.middleware.cors import CORSMiddleware

import string
from fastapi import  Request, Response, HTTPException, status, UploadFile, Form, middleware
from constant import ALGORITHM, SECRET_KEY
from jose import jwt, JWTError

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.client = MONGODB
# app.db = app.client
app.db = MONGODB

app.include_router(auth_router, tags=["login"], prefix="/auth")

@app.middleware("http")
async def verify_token(request:Request,call_next):
    if "authorization" in request.headers.keys():
        try:
            raw = request.headers["authorization"].split(' ')[-1]
            payload = jwt.decode(raw, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.username: str = payload["sub"]
            request.state.id: str = payload["id"]
        except Exception as error:
            # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=error)
            print("ok")
    response = await call_next(request)
    return response

app.include_router(subject_router, tags=["subject"], prefix="/subject")
app.include_router(video_router, tags=["video"], prefix="/video")
app.include_router(result_router, tags=["result"], prefix="/result")



