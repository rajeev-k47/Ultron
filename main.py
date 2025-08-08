from fastapi import FastAPI
from audio import Buzzer, Speaker
from fastapi.responses import StreamingResponse
from apscheduler.schedulers.background import BackgroundScheduler
from lights import HeadLight, LDR, Decor, TubeLight
from state.state import State
from video import VideoStream, People
import threading
from dotenv import load_dotenv
import os
import cv2
from voice import WakeListener
from gen_ai import Groqy

load_dotenv()
PASSWORD = os.getenv("PASSWORD")
ACCESS = int(os.getenv("ACCESS", 0))
ACCESS_KEY = os.getenv("ACCESS_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

camera = cv2.VideoCapture(0)
app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()
groq = Groqy(api_key=GROQ_API_KEY)
state = State()
state.init_file()
buzzer = Buzzer(pin=16)
headlight = HeadLight(pin=6, state=state)
ldr = LDR(pin=4, headlight=headlight)
decor = Decor(pin=12, state=state)
tubelight = TubeLight(pin=17, state=state)
# people_detector = People(cap=camera)
listener = WakeListener(
    access_key=ACCESS_KEY,
    buzzer=buzzer,
    headlight=headlight,
    tubelight=tubelight,
    state=state,
    groqy=groq,
    keywords=["terminator"],
)


@app.on_event("startup")
def bg_tasks():
    thread = threading.Thread(target=ldr.read, daemon=True)
    # thread1 = threading.Thread(target=people_detector.run, daemon=True)
    thread2 = threading.Thread(target=listener.listen, daemon=True)
    thread2.start()
    # thread1.start()
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
    cam1 = VideoStream()
    return StreamingResponse(
        cam1.generate_frames(camera),
        media_type="multipart/x-mixed-replace;boundary=frame",
    )


@app.get("/tempvideo")
def stream_temp():
    global ACCESS
    if ACCESS < 0:
        return {"st": "Temp limit reached"}
    ACCESS -= 1
    buzzer.alert()
    cam2 = VideoStream()
    return StreamingResponse(
        cam2.generate_frames(camera),
        media_type="multipart/x-mixed-replace;boundary=frame",
    )


@app.get("/headlight")
def toggleHeadlight(mode: int = 0):
    state.update_state("headlight", mode)
    if mode != 0:
        headlight.status = mode
        return {"st": "Headlight set to mode " + str(mode)}
    headlight.status = 0
    headlight.toggle()
    return {"st": "Headlight toggled"}


@app.get("/tubelight")
def toggleTubeLight(fun: int = 0):
    if fun != 0:
        tubelight.fun()
        return {"st": "Let's have some fun"}
    tubelight.toggle()
    return {"st": "TubeLight toggled"}


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
    tubelight.cleanup()
