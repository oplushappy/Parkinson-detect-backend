# mongo-fastapi

## Goal
Achieve a website it can help old people to detect parksion.

## front end
[DACHXY/parkinson](https://github.com/DACHXY/parkinson)

## How to use :
1. quick to see backend
```
cd src
uvicorn main:app --reload
```

2. quick to open website :

run on linux enviromeent

revise mongodb part to use yourself account

`pip install -r requirements.txt`

open the front end

`uvicorn main:app --host x.x.x.x --port 52697`

## Functions
1. Sign Up :
It will sent email to verify

2. Sign In

3. Change Password :
It will sent email to verify

4. Change Name :
Can direct revise

5. Upload Video :
Vedio will play if mouse put in vedio

6. List Videos and Show Results
Will sort by date and have a filter 

7. Change Video Information
you can change your name, date

8. Show the Activity of Parkinson in Taiwan

## Openpose model :

1. Detect 手指拍打 手掌握合 抬腳 前臂迴旋

2. Upload a Video with some Action , it will return a value 
