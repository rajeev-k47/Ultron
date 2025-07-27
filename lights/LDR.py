import RPi.GPIO as GPIO
import time
from lights.HeadLight import HeadLight


class LDR:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)
        self.pin = pin

    def cleanup(self):
        GPIO.cleanup(self.pin)

    def read(self):
        headLight = HeadLight(6)
        while True:
            GPIO.setup(self.pin, GPIO.OUT)
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(0.1)

            GPIO.setup(self.pin, GPIO.IN)
            currentTime = time.time()

            diff = 0
            while GPIO.input(self.pin) == GPIO.LOW:
                diff = time.time() - currentTime

            if (diff * 1000) > 100:
                headLight.on()
            else:
                headLight.off()

            time.sleep(1)
