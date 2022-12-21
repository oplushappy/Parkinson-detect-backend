# import logging
# from fastapi.responses import JSONResponse
# # import openposeTest
from fastapi import APIRouter, Request, Form, status, UploadFile, BackgroundTasks
import os
from moviepy.editor import * 
from subject.method import form_change_to_json
from fastapi.encoders import jsonable_encoder
import uuid
import pathlib
#these is in linux server
import gpu_tool as gt 
import preprocess as pp
import rotation as ra
import leg
import fingertapping as ft
import handmovement as hm
import os
import subprocess
from subject.method import form_change_to_json
from tool.colorprint import Cprint, bcolor

router = APIRouter()

def define_detect_type(detect):
    if (detect == '手指拍打'):
        return 't23'
    if (detect == '手掌握合'):
        return't24' 
    if (detect == '前臂迴旋'):
        return 't25'
    if (detect == '抬腳'):
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
async def upload(background_tasks:BackgroundTasks,request: Request, information: str = Form(), file: UploadFile = Form()):    
    save_path = "../testdir/files"
    information = form_change_to_json(information)

    contents = file.file.read()
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
        # while contents := file.file.read(1024*1024):
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
    
    #Todo
    # background_tasks.add_task(
    #
    # )
    openpose_result = process(video_name)
    request.app.db.video.find_one_and_update(
      {"user_id": request.state.id},
      {"$set": {"left": openpose_result[0].get('left'),
                "right": openpose_result[0].get('right')}},
        upsert=True
    )
    return status.HTTP_201_CREATED


# @router.post("/uploadFile/fake",status_code=status.HTTP_201_CREATED)
# async def upload(request: Request, information: str = Form(), file: UploadFile = Form()):
# # def upload(file : UploadFile, date: str, detect_type: str, user_id: str):
#     img_bytes = await file.read()
#     img_name = file.filename
#     save_path = "./testdir/files"
                  
#     if not os.path.exists(save_path):
#         os.mkdir(save_path)
#     with open('{}/{}'.format(save_path ,img_name), "wb") as f:
#         f.write(img_bytes)

#     information = form_change_to_json(information);    
#     if (information["detect"] == 'FT'):
#         file_type = 't23'
#     elif (information["detect"] == 'HM'):
#         file_type = 't24' 
#     elif (information["detect"] == 'LA'):
#         file_type = 't25'
#     elif (information["detect"] == 'RAMOH'):
#         file_type = 't26'
#     else:
#         return status.HTTP_400_BAD_REQUEST 
    
#     os.chdir("./testdir/files/")
#     video = VideoFileClip(img_name)
#     video_id = uuid.uuid4()
#     output = video.copy()
#     output.write_videofile(f'{information["date"]}_{video_id}_{file_type}.mov',temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
#     video_name = f'{information["date"]}_{video_id}_{file_type}.mov'
#     os.chdir('../../')
    
#     openpose_result = process(video_name)
    
#     path = str(pathlib.Path(video_name).absolute())
#     result_video = {
#         "user_id": request.state.id,
#         "subject": information["name"],
#         "gender":information["gender"],
#         "detect":information["detect"],
#         "date": information["date"],
#         "location": information["location"],
#         "video_name": video_name,
#         "video_path": path,
#         # "left": openpose_result[0]['left'],
#         # "right": openpose_result[0]['right']
#         "left": openpose_result[0].get('left'),
#         "right": openpose_result[0].get('right'),
#     }
#     result = request.app.db.video.insert_one(result_video) 
#     return status.HTTP_200_OK


def process(video_name : str):
    video_read_path = './testdir/files/'
    video_cv_path = './testdir/cv/'
    #video_openpose_path = './testdir/op/'
    video_json_path = './testdir/js/'
    file_name = video_name
    
    print('file name :', file_name)
    
    types = gt.type_mux(file_name)
    gt.check_file(file_name, video_read_path)
   
    cv_target = pp.videoPreProcess(file_name, video_read_path, video_cv_path)
    num_str = gt.get_gpu_free()
    # 路徑的資料夾要事先創建好
    # videoPreProcess(檔案名稱,原影片路徑,前處理後影片放置路徑)
    # gt.push_queue(file_name)
    # num_str = gt.check_gpu_free()
    # while((num_str is None) or (gt.get_queue() != file_name)):
    #     time.sleep(1)
    #     print('waiting...')
    #     num_str = gt.check_gpu_free()
    #     pass
    # gt.pull_queue()
    # print('gpu_free =', num_str)
    #pp.videoDoOpenpose(file_name, cv_target, video_json_path,num_str)
    pp.videoDoOpenpose(file_name, cv_target, video_json_path,str(num_str))
    # 當GPU皆為繁忙時，會每5秒讀取空閒顯卡，直到讀取到空閒顯卡為止
    #loadManyJsonFolder(檔案名稱,json資料夾路徑,txt存放路徑,結果是否繪圖,是否將繪圖存檔)
    #result = openposeTest.loadManyJsonFolder(file_name, './testdir/js/', './testdir/txt/', False, False)
    
    if(types == 23):
        result = ft.loadManyJsonFolder(file_name,video_json_path)
    elif(types == 24):
        result = hm.loadManyJsonFolder(file_name,video_json_path)
    elif(types == 25):
        result = ra.loadManyJsonFolder(file_name,video_json_path)
    elif(types == 26):
        result = leg.loadManyJsonFolder(file_name,video_json_path)
    else:
        result = [{"left": 0, "right": 0 }]
    
    
    json_compatible_item_data = jsonable_encoder(result)
    
    # gt.cleanFile(video_read_path,file_name)
    #clean original file to release space
    #cv_file = "CV"+file_name[:-4]+'.avi'
    #gt.cleanFile(video_cv_path,cv_file)
    #clean cv file to release space

    # print(JSONResponse(json_compatible_item_data))
    # new_result = MONGODB.result.insert_one(json_compatible_item_data)
    # created_result = MONGODB.result.find_one(
    #     {"_id": new_result.inserted_id}
    # )
    
    # MONGODB.result.insert_one(created_result)
    
    # r = requests.post('https://localhost:34567/upload/a89d9ebc034c0dbe8fa3f/',data=json_compatible_item_data)
    return json_compatible_item_data

