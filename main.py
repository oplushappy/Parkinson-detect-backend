from fastapi import FastAPI
from pymongo import MongoClient

from subject import router as subject_router
from result import router as result_router
from video import router as video_router
from login import router as login_router

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

app.client = MongoClient("mongodb+srv://ken:a12345678a@angry.daaorae.mongodb.net/?retryWrites=true&w=majority")
# app.client = MongoClient()
app.db = app.client.angry

app.include_router(login_router, tags=["login"], prefix="/login")
app.include_router(subject_router, tags=["subject"], prefix="/subject")
app.include_router(video_router, tags=["video"], prefix="/video")
app.include_router(result_router, tags=["result"], prefix="/result")



