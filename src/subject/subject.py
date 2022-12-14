
import datetime

import string
import pymongo
from bson import ObjectId
from fastapi import APIRouter, Body, Request, Response, HTTPException, status, UploadFile, Form, middleware, FastAPI
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid

from subject.model import Subject, Video, UserPersonalData
from subject.method import *

# app = FastAPI()
router = APIRouter()

from bson.objectid import ObjectId



@router.post("/user_personal", response_description="user personal data",status_code=status.HTTP_201_CREATED)
def create_user(request: Request, information: UserPersonalData = Form()):
    information = form_change_to_json(information)
    user = {
        "full_name": information["name"],
        "gender": information["gender"],
        "age": information["age"],
        "email": information["email"]
    }
    new_user = request.app.db.users.find_one_and_update({"_id" : request.state.id},{ "$set": {user} })
    return new_user

#列出測試者所有影片
@router.get("/list/video", response_model=List[Video], response_description="list all video about subject",status_code=status.HTTP_200_OK)
def list_video(request: Request):
    try:
        print(request.state.id)
    except:
        return "not ok"
    test = request.app.db.video.find({"user_id": request.state.id}, limit=100).sort("date", pymongo.ASCENDING)
    test2 = []
    for i in test:
        i["video_id"] = str(i["_id"])
        test2.append(Video(**i))
    return test2
    

#修改影片
@router.put("/update/video",response_model = Video, response_description="do some change in video",status_code=status.HTTP_200_OK)
def update_video(request: Request, information: str = Form()):#video_id: str, date: datetime.date, location: str
    information = form_change_to_json(information)
    updated_video = request.app.db.video.find_one_and_update(
        {"_id": ObjectId(information["video_id"])},
        {"$set": {"subject":information["name"],
                    "gender":information["gender"],
                    "detect":information["detect"],
                    "date": information["date"], 
                    "location": information["location"]}},
        upsert=True
    )
    updated_video["video_id"] = str(updated_video["_id"])
    return Video(**updated_video)

#刪除影片紀錄
@router.delete("/delete/video", response_description="Delete a video",status_code=status.HTTP_202_ACCEPTED)
def delete_video(request: Request, video_id: str):
    delete_result = request.app.db.video.find_one_and_delete({
        "user_id": request.state.id,
        "_id": ObjectId(video_id)
    })
    if delete_result:
        return status.HTTP_202_ACCEPTED
    raise HTTPException(status_code=404, detail="video not exist")

