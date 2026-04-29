from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from instagrapi import Client
import os

app = FastAPI()

class LoginData(BaseModel):
    username: str
    password: str

class TaskData(BaseModel):
    username: str
    password: str
    action: str  # "follow" or "like"
    target_username: str
    count: int = 10

@app.get("/")
def root():
    return {"status": "ok", "message": "IG Bot Running"}

@app.post("/login")
def login(data: LoginData):
    cl = Client()
    try:
        cl.login(data.username, data.password)
        user_info = cl.user_info_by_username(data.username)
        return {
            "status": "success",
            "user_id": str(user_info.pk),
            "full_name": user_info.full_name,
            "avatar_url": str(user_info.profile_pic_url)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/do-task")
def do_task(data: TaskData):
    cl = Client()
    try:
        cl.login(data.username, data.password)
        target = cl.user_info_by_username(data.target_username)
        
        if data.action == "follow":
            cl.user_follow(target.pk)
            return {"status": "success", "action": "followed", "target": data.target_username}
        
        elif data.action == "like":
            medias = cl.user_medias(target.pk, amount=data.count)
            liked = 0
            for media in medias:
                cl.media_like(media.id)
                liked += 1
            return {"status": "success", "action": "liked", "count": liked}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/user-info/{username}")
def get_user_info(username: str):
    cl = Client()
    try:
        info = cl.user_info_by_username_v1(username)
        return {
            "username": username,
            "full_name": info.full_name,
            "avatar_url": str(info.profile_pic_url),
            "followers": info.follower_count
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
