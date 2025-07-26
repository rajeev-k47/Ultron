import RPi.GPIO as GPIO
import time


class Buzzer:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.pin = pin

    def cleanup(self):
        GPIO.cleanup(self.pin)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def peeb(self, duration=0.2):
        self.on()
        time.sleep(duration)
        self.off()

    def repeat(self, times=3, interval=0.3):
        for _ in range(times):
            self.peeb()
            time.sleep(interval)

    def alert(self):
        self.peeb(0.5)
        time.sleep(0.2)
        self.peeb(0.2)
        time.sleep(0.2)
        self.peeb(0.5)

    def sauce(self):
        short = 0.2
        long = 0.6
        gap = 0.2

        for _ in range(3):
            self.peeb(short)
            time.sleep(gap)
        time.sleep(0.6)

        for _ in range(3):
            self.peeb(long)
            time.sleep(gap)
        time.sleep(0.6)

        for _ in range(3):
            self.peeb(short)
            time.sleep(gap)
