from fastapi import FastAPI
from database import MONGODB
from subject.subject import router as subject_router
from result import router as result_router
from video import router as video_router
from auth.auth import router as auth_router

from fastapi.middleware.cors import CORSMiddleware

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
app.include_router(subject_router, tags=["subject"], prefix="/subject")
app.include_router(video_router, tags=["video"], prefix="/video")
app.include_router(result_router, tags=["result"], prefix="/result")



