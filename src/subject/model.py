import datetime
from pydantic import BaseModel, Field


class Subject(BaseModel):
    subject: str
    gender: str
    age: int = Field(..., gt=0, lt=100)

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