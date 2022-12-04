import json
from bson import ObjectId
from fastapi import UploadFile, Request, APIRouter, Form, status
from typing import List
import os
import uuid
import pathlib
import  datetime

from fastapi.encoders import jsonable_encoder

from model import Video
from auth.method import get_current_user
from subject.method import decode_jwt

router = APIRouter()

# @router.post("/download")
# def download_video(user_id: str, video_id: str, request: Request):
#     find_video = request.app.db.video.find_one({
#         "owner_id": user_id,
#         "_id": ObjectId(video_id)
#     })
#     return find_video

@router.post("/uploadFile/fake")
async def upload(request: Request, information: str = Form(), file: UploadFile = Form()):
    video = await file.read() #.file
    video_name = file.filename
    save_path = "../testdir/files"

    if not os.path.exists(save_path):
        os.mkdir(save_path)
    with open('{}/{}'.format(save_path ,video_name), "wb") as f:
        f.write(video)
    
    information = json.loads(information)
    # jwt_token = information["access_token"]
    # print(await get_current_user(jwt_token))

    username = decode_jwt(information)


    path = jsonable_encoder(pathlib.Path(video_name).absolute())
    date = jsonable_encoder(information["date"])
    video = {
        "subject": username,
        "video_name": video_name,
        "video_path": path,
        "date": date,
        "location": information["location"]
    }
    result = request.app.db.video.insert_one(video)
    return "ok"



