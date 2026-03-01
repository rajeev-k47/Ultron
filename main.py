from rpi_ws281x import Color
from door.read import DoorReader
from fastapi import FastAPI, Query
from audio import Buzzer, Speaker, StreamPlayer
from fastapi.responses import StreamingResponse
from apscheduler.schedulers.background import BackgroundScheduler
from lights import HeadLight, LDR, Decor, TubeLight
from matrix.write import Matrix
from state.state import State
from video import video_stream
import threading
from dotenv import load_dotenv
import os
import time
import cv2
from voice import WakeListener
from gen_ai import Groqy
from lights import Strip
from mqtts import mqtts
from matrix import SerialComm

load_dotenv()
PASSWORD = os.getenv("PASSWORD")
ACCESS = int(os.getenv("ACCESS", 0))
ACCESS_KEY = os.getenv("ACCESS_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MQTTS_USER = os.getenv("MQTTS_USER")
MQTTS_PASS = os.getenv("MQTTS_PASS")

app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()

speaker = Speaker(GROQ_API_KEY)

groq = Groqy(api_key=GROQ_API_KEY, speaker=speaker)

state = State()
state.init_file()

buzzer = Buzzer(pin=16)
headlight = HeadLight(pin=6, state=state)
ldr = LDR(pin=4, headlight=headlight)
decor = Decor(pin=12, state=state)
tubelight = TubeLight(pin=17, state=state)
matrix = Matrix()
streamplayer = StreamPlayer(matrix)
door = DoorReader(tubelight)
# people_detector = People(cap=camera)
strips = Strip()
serialcomm = SerialComm()
mqtts = mqtts(MQTTS_USER, MQTTS_PASS, tubelight, serialcomm)

from audio.AudioRecorder import audio_recorder

listener = WakeListener(
    access_key=ACCESS_KEY,
    buzzer=buzzer,
    headlight=headlight,
    tubelight=tubelight,
    state=state,
    groqy=groq,
    speaker=speaker,
    streamplayer=streamplayer,
    keywords=["terminator"],
)


def generate_frames():
    while True:
        frame = video_stream.get_frame()
        if frame is None:
            continue
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
        time.sleep(0.03)


@app.on_event("startup")
def bg_tasks():
    thread = threading.Thread(target=ldr.read, daemon=True)
    thread2 = threading.Thread(target=listener.listen, daemon=True)
    thread3 = threading.Thread(target=door.read, daemon=True)
    thread4 = threading.Thread(target=mqtts.publish_status, daemon=True)
    thread5 = threading.Thread(target=serialcomm.read, daemon=True)
    thread2.start()
    thread3.start()
    thread.start()
    thread4.start()
    thread5.start()


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


@app.get("/strip")
def strip(m: int):
    strips.rpm(m)
    return {"st": "Ok"}

@app.get("/strip/color")
def set_strip_color(r: int, g: int, b: int):
    strips.set_color(r, g, b)
    return {"st": f"Color set to {r},{g},{b}"}

@app.get("/alarm")
def schedule_alarm(
    hour: int = Query(...),
    minute: int = Query(...),
    password: str = Query(...),
    wakeup: bool = Query(False),
):
    if password != PASSWORD:
        return {"st": "Unauthorized"}

    scheduler.add_job(buzzer.repeat, "cron", hour=hour, minute=minute, args=[40, 0.4])

    if wakeup:
        scheduler.add_job(tubelight.fun, "cron", hour=hour, minute=minute, args=[])

    return {"st": f"Alarm set at {hour}:{minute}"}

@app.get("/door")
def door_switch(value: str):
    door.write(value)
    return {"st": f"Door set to {value}"}

@app.get("/matrix")
def matrix_switch(value: int):
    matrix.write(value)
    return {"st": f"Matrix set to {value}"}


@app.get("/video")
def stream(password: str):
    if password != PASSWORD:
        return {"st": "Unauthorized"}
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace;boundary=frame",
    )


@app.get("/tempvideo")
def stream_temp():
    global ACCESS
    if ACCESS < 0:
        return {"st": "Temp limit reached"}
    ACCESS -= 1
    buzzer.alert()
    return StreamingResponse(
        generate_frames(),
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
def toggleTubeLight(fun: int = -1):
    if fun == 0:
        tubelight.off()
        return {"st": "TubeLight turned off"}
    elif fun == 1:
        tubelight.on()
        return {"st": "TubeLight turned on"}
    elif fun == -1:
        tubelight.toggle()
        return {"st": "TubeLight toggled"}
    else:
        tubelight.fun()
        return {"st": "Let's have some fun"}


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
