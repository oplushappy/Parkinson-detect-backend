from fastapi import UploadFile, Request, APIRouter, Form, status
import os
import uuid
import subprocess
from subject.method import form_change_to_json
from tool.colorprint import Cprint, bcolor


router = APIRouter()

def define_detect_type(detect):
    if (detect == '手指拍打'):
        return 't23'
    if (detect == '手掌握合'):
        return't24' 
    if (detect == '抬腳'):
        return 't25'
    if (detect == '前臂迴旋'):
        return 't26'
    raise status.HTTP_400_BAD_REQUEST 

def generate_video_name(date, detect, ext):
    return "{}_{}_{}.{}".format(
        date, 
        uuid.uuid4() , 
        define_detect_type(detect),
        ext
    )

@router.post("/uploadFile/fake")
async def upload(request: Request, information: str = Form(), file: UploadFile = Form()):

    
    save_path = "../testdir/files"
    information = form_change_to_json(information)

    # naming
    VIDEO_EXT = "mov"
    video_name = generate_video_name(
        information.get("date").replace(" ", "-").replace(":", "-"), 
        information.get("detect"),
        VIDEO_EXT
    )
    Cprint("text", bcolor.HEADER)

    print("Start to save file")
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    with open('{}/{}'.format(save_path ,video_name), "wb") as f:
        while contents := file.file.read(1024*1024):
            f.write(contents)
    print("File Saved")


    path = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
    path = os.path.join(path, "testdir", "files", video_name)
    path = str(path)
    thumbnail_path = path.rsplit(".", 1)[0] + "_thumbnail.jpg"
    print(path, "\n", thumbnail_path)
    print("Dealing with ffmpeg thumbnail proccess")
    subprocess.run(["ffmpeg", "-i", path, "-ss", "3", "-vframes", "1", thumbnail_path])
    print("Complete!")

    video = {
        "user_id": request.state.id,
        "subject": information["name"],
        "gender":information["gender"],
        "detect":information["detect"],
        "date": information["date"],
        "location": information["location"],
        "video_name": video_name,
        "video_path": path,
        "thumbnail_path": thumbnail_path,
        "left": 0,
        "right": 0
    }
    result = request.app.db.video.insert_one(video) 
    return status.HTTP_201_CREATED



