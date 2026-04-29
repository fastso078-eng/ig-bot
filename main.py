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
    target_username: str
    action: str  # "follow" or "like"
    count: int = 10

@app.get("/")
def root():
    return {"status": "ok", "message": "ig-bot is running"}

@app.post("/login")
def login(data: LoginData):
    cl = Client()
    try:
        cl.login(data.username, data.password)
        return {"status": "success", "message": "Logged in successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/do-task")
def do_task(data: TaskData):
    cl = Client()
    try:
        cl.login(data.username, data.password)
        
        if data.action == "follow":
            user_id = cl.user_id_from_username(data.target_username)
            cl.user_follow(user_id)
            return {"status": "success", "action": "follow", "target": data.target_username}
        
        elif data.action == "like":
            user_id = cl.user_id_from_username(data.target_username)
            medias = cl.user_medias(user_id, data.count)
            liked = 0
            for media in medias:
                cl.media_like(media.id)
                liked += 1
            return {"status": "success", "action": "like", "liked_count": liked}
        
        else:
            raise HTTPException(status_code=400, detail="Invalid action")
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
