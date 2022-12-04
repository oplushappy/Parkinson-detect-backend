from fastapi import APIRouter, Body, Request, Response, HTTPException, status, UploadFile
from fastapi.encoders import jsonable_encoder
from typing import List

from model import Result

router = APIRouter()

# # @router.post()
# def detect_type(type: str):


@router.post("/")
def save_result(request: Request, result: Result):
    result = result.dict()
    new_result = request.app.db.result.insert_one(result)
    created_result = request.app.db.result.find_one(
        {"_id": new_result.inserted_id}
    )
    return created_result

