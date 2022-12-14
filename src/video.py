import json
from bson import ObjectId
from fastapi import UploadFile, Request, APIRouter, Form, status
from typing import List
import os
import uuid
import pathlib
import  datetime

from fastapi.encoders import jsonable_encoder

from subject.model import Video
from auth.method import get_current_user
from subject.method import decode_jwt

from subject.method import form_change_to_json

router = APIRouter()

@router.post("/uploadFile/fake")
async def upload(request: Request, information: str = Form(), file: UploadFile = Form()):
    video = await file.read() #.file
    video_name = file.filename
    save_path = "../testdir/files"

    print("Start to save file")
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    with open('{}/{}'.format(save_path ,video_name), "wb") as f:
        f.write(video)
    print("File Saved")

    information = form_change_to_json(information)
    path = str(pathlib.Path(video_name).absolute())
    video = {
        "user_id": request.state.id,
        "subject": information["name"],
        "gender":information["gender"],
        "detect":information["detect"],
        "date": information["date"],
        "location": information["location"],
        "video_name": video_name,
        "video_path": path
    }
    print(video)
    result = request.app.db.video.insert_one(video) 
    return status.HTTP_201_CREATED



