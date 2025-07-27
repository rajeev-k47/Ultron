from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from apscheduler.schedulers.background import BackgroundScheduler
from audio import Buzzer
from video import VideoStream

from dotenv import load_dotenv
import os

load_dotenv()
PASSWORD = os.getenv("PASSWORD")
ACCESS = int(os.getenv("ACCESS", 0))

app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()

buzzer = Buzzer(pin=16)


@app.get("/")
def home():
    return {
        "Endpoints": {
            "alarm": "/alarm",
            "video": "/video",
            "tempvideo": "/tempvideo",
        }
    }


@app.post("/alarm")
def schedule_alarm(hour: int, minute: int, password: str):
    if password != PASSWORD:
        return {"st": "Unauthorized"}
    scheduler.add_job(buzzer.repeat, "cron", hour=hour, minute=minute, args=[20, 0.7])
    return {"st": f"Alarm set at {hour}:{minute}"}


@app.get("/video")
def stream(password: str):
    if password != PASSWORD:
        return {"st": "Unauthorized"}
    camera = VideoStream()
    return StreamingResponse(
        camera.generate_frames(),
        media_type="multipart/x-mixed-replace;boundary=frame",
    )


@app.get("/tempvideo")
def stream_temp():
    global ACCESS
    if ACCESS < 0:
        return {"st": "Temp limit reached"}
    ACCESS -= 1
    buzzer = Buzzer(pin=16)
    buzzer.alert()
    camera = VideoStream()
    return StreamingResponse(
        camera.generate_frames(),
        media_type="multipart/x-mixed-replace;boundary=frame",
    )
