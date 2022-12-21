from fastapi import APIRouter, Request
from activity.method import scrpy

router = APIRouter()

@router("/list/activity")
def list_activity(request: Request):
  scrpy(request.app.db.url)
  cursor = request.app.db.url.find({})
  result = []
  for document in cursor:
    result.append(document)
  return result