from fastapi import UploadFile, Request, APIRouter
from typing import List
import os
import uuid
import pathlib
import  datetime

from fastapi.encoders import jsonable_encoder

from model import Video

router = APIRouter()

@router.post("/uploadFile/{id}")
def upload(id: str, request: Request, files: List[UploadFile], date: datetime.date, location: str):#, video: Video
    for singleFile in files:
        imgBytes = singleFile.file.read()
        imgname = singleFile.filename
        save_path = "./testdir/files"

        if not os.path.exists(save_path):
            os.mkdir(save_path)
        with open('./testdir/files/{}'.format(imgname), "wb") as f:
            f.write(imgBytes)

        path = jsonable_encoder(pathlib.Path(imgname).absolute())
        date = jsonable_encoder(date)
        location = jsonable_encoder(location)
        # # request.app.db.user.find_one()
        request.app.db.vedio.insert_one({
            "owner_id": id,
            "video_name": imgname,
            "video_path": path,
            "date": date,
            "location": location
        })
    return True



