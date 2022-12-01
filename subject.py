from fastapi import APIRouter, Body, Request, Response, HTTPException, status, UploadFile
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid

from model import Subject

router = APIRouter()



#創建一組測試者資料
@router.post("/",response_model=Subject, response_description="create test data",status_code=status.HTTP_201_CREATED)
def create_subject(request: Request, subject: Subject):
    # subject = subject.dict()
    subject = jsonable_encoder(subject)
    new_subject = request.app.db.user.insert_one(subject)
    created_subject = request.app.db.user.find_one(
        {"_id": new_subject.inserted_id}
    )
    return created_subject

#列出測試者所有相關資料+ 影片
@router.get("/{id}",response_model=Subject, response_description="list all vedio about subject")
def list_data(id: str, request: Request):
    if (subject := request.app.db.user.find({"_id": id})) is not None:
        return subject
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"subject with id {id} not found")


#刪除影片紀錄
@router.delete("/{id}/video/{id2}", response_description="Delete a video")
def delete_video(id: str, id2: str, request: Request, response: Response):
    delete_result = request.app.db.vedio.delete_one(
        {"_id": id2,
         "owner_id": id}
    )
    # delete_result = old_video.delete #?delete update

    # if delete_result.deleted_count == 0:
    #     response.status_code = status.HTTP_204_NO_CONTENT
    #     return response
    #
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vedio with ID {id} not found")


