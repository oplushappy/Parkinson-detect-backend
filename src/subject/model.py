import datetime
from pydantic import BaseModel, Field


class Subject(BaseModel):
    subject: str
    gender: str
    age: int = Field(..., gt=0, lt=100)

class UserPersonalData(BaseModel):
    real_name: str
    gender: str
    age: int = Field(..., gt=0, lt=100)

class Video(BaseModel):
    video_id: str
    user_id: str
    subject: str
    gender: str
    detect: str
    video_name: str
    video_path: str    
    thumbnail_url: str
    date: str
    location: str
    left: str
    right: str
    