# Parkinson Detect Website

## Goal
Achieve a website it can help old people to detect parksion.

## front end
[DACHXY/parkinson](https://github.com/DACHXY/parkinson)

## Download
Because file 400 MB , so I put the full version in google cloud
[parkinson-project.zip](https://drive.google.com/file/d/1L6M6fWrNMYweD8bYPfMhdl8FhOKVppI3/view)

## How to use :
1. quick to see backend
```
cd src
uvicorn main:app --reload
```

2. quick to open website :
- run on linux enviromeent
- cd run_on_linux/src
- revise mongodb part to use yourself account
- `pip install -r requirements.txt`
- open the front end
- `uvicorn main:app --host x.x.x.x --port 52697`

## How to implement:
- React
- Pytorch with Caffe
- FastApi
- MongoDB(pymongo)
- Openpose


## Functions

detail in auth (Dir)
1. Sign Up : sent email to verify and create account
2. Sign In : By username and password
3. Change Password :sent email to verify and then revise password
4. Change Name : revise user name

detail in subject.py and video_result (Dir)
5. Upload Video : Vedio will play if mouse put in vedio
6. List Videos and Show Results : which sort by date and have a filter 
7. Change Video Information: change user name, date, detect place

detail in activity (Dir)
8. Show the Activity of Parkinson in Taiwan

## Openpose model :

1. Detect 手指拍打 手掌握合 抬腳 前臂迴旋

2. Upload a Video with corresponding Action , Age , gender, it will return a value. 
