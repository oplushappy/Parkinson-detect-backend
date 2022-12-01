import datetime
from pydantic import BaseModel, Field
from fastapi import UploadFile
from typing import List

class Subject(BaseModel):
    subject: str
    gender: str
    age: int = Field(..., gt=0, lt=100)
    # date: datetime.date
    # location: str
    # other_condition: str | None = None
    # vedio: UploadFile
    # vedio_name: str = None


class Result(BaseModel):
    left: int
    right: int

class Video(BaseModel):
    owner_id: str
    video_name: str
    video_path: str
    date: datetime.date
    location: str

    class Config:
        schema_extra = {
            "example": {
                "date": "2022-10-23",
                "location": "hospital"
            }
        }
