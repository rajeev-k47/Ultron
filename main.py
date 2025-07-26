from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from audio import Buzzer

from dotenv import load_dotenv
import os

load_dotenv()
PASSWORD = os.getenv("PASSWORD")

app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()

buzzer = Buzzer(pin=16)


@app.get("/")
def home():
    return {"st": "Server running"}


@app.post("/alarm")
def schedule_alarm(hour: int, minute: int, password: str):
    if password != PASSWORD:
        return {"st": "Unauthorized"}
    scheduler.add_job(buzzer.repeat, "cron", hour=hour, minute=minute, args=[20, 0.7])
    return {"st": f"Alarm set at {hour}:{minute}"}
