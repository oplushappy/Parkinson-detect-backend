import datetime

import pymongo
from bson import ObjectId
from fastapi import APIRouter, Body, Request, Response, HTTPException, status, UploadFile
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid

from model import Subject, Video

router = APIRouter()

from bson.objectid import ObjectId


#創建一組測試者資料
@router.post("/", response_model=Subject, response_description="create test data",status_code=status.HTTP_201_CREATED)
def create_subject(request: Request, subject: Subject):
    # subject = subject.dict()
    subject = jsonable_encoder(subject)
    new_subject = request.app.db.user.insert_one(subject)
    created_subject = request.app.db.user.find_one(
        {"_id": new_subject.inserted_id}
    )
    return created_subject

#列出測試者所有相關資料
@router.get("/{user_id}",response_model=Subject, response_description="list all data about subject",status_code=status.HTTP_200_OK)
def list_data(user_id: str, request: Request):
    if (subject := request.app.db.user.find_one({"_id": ObjectId(user_id)})) is not None:
        return subject
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"subject with id {id} not found")

#列出測試者所有影片
@router.get("/video/{user_id}", response_model=List[Video], response_description="list all video about subject",status_code=status.HTTP_200_OK)
def list_video(user_id: str, request: Request):
    video = list(request.app.db.vedio.find({"owner_id": user_id}, limit=100).sort("date", pymongo.ASCENDING))
    return video
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"video with id {user_id} not found")

#修改影片
@router.post("/update/{video_id}",response_model = Video, response_description="do some change in video",status_code=status.HTTP_200_OK)
def update_video(video_id: str, date: datetime.date, location: str, request: Request):
    date = jsonable_encoder(date)
    updated_video = request.app.db.vedio.update_one(
        {"_id": ObjectId(video_id)},
        {"$set": {"date": date, "location": location}},
        upsert=True
    )
    return updated_video

#刪除影片紀錄
@router.delete("/{owner_id}/video/{video_id}", response_description="Delete a video",status_code=status.HTTP_200_OK)
def delete_video(owner_id: str, video_id: str, request: Request):
    delete_result = request.app.db.vedio.delete_one({
        "owner_id": owner_id,
        "_id": ObjectId(video_id)
    })
    return delete_result

    # if delete_result.deleted_count == 0:
    #     response.status_code = status.HTTP_204_NO_CONTENT
    #     return response
    #
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vedio with ID {id} not found")


