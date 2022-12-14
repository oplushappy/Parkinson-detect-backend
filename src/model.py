import datetime
from pydantic import BaseModel, Field
from fastapi import UploadFile
from typing import List, Optional, Union


class Subject(BaseModel):
    subject: str
    gender: str
    age: int = Field(..., gt=0, lt=100)


class Result(BaseModel):
    left: int
    right: int

class Video(BaseModel):
    user_id: str
    video_name: str
    video_path: str
    date: datetime.date
    location: str


