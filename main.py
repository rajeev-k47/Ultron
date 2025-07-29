from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from apscheduler.schedulers.background import BackgroundScheduler
from audio import Buzzer
from lights import HeadLight, LDR, Decor
from video import VideoStream
import threading
from dotenv import load_dotenv
import os

load_dotenv()
PASSWORD = os.getenv("PASSWORD")
ACCESS = int(os.getenv("ACCESS", 0))

app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()

buzzer = Buzzer(pin=16)
headlight = HeadLight(pin=6)
ldr = LDR(pin=4, headlight=headlight)
decor = Decor(pin=12)


@app.on_event("startup")
def bg_tasks():
    thread = threading.Thread(target=ldr.read, daemon=True)
    thread.start()


@app.get("/")
def home():
    return {
        "Endpoints": {
            "alarm": "/alarm",
            "video": "/video",
            "tempvideo": "/tempvideo",
            "decor": "/decor",
            "headlight": "/headlight",
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


@app.get("/headlight")
def toggleHeadlight(mode: int = 0):
    if mode != 0:
        headlight.status = mode
        return {"st": "Headlight set to mode " + str(mode)}
    headlight.status = 0
    headlight.toggle()
    return {"st": "Headlight toggled"}


@app.get("/decor")
def toggleDecor(mode: int):
    decor.setmode(mode)
    return {"st": "Decor set to mode " + str(mode)}


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
    ldr.cleanup()
    buzzer.cleanup()
    headlight.cleanup()
    decor.cleanup()
