import RPi.GPIO as GPIO
import time
from lights.HeadLight import HeadLight
# Subclass HeadLight (STATUS:1)


class LDR:
    def __init__(self, pin, headlight: HeadLight):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)
        self.pin = pin
        self.headlight = headlight

    def cleanup(self):
        GPIO.cleanup(self.pin)

    def read(self):
        while True:
            if self.headlight.status != 1:
                continue
            GPIO.setup(self.pin, GPIO.OUT)
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(0.1)

            GPIO.setup(self.pin, GPIO.IN)
            currentTime = time.time()

            diff = 0
            while GPIO.input(self.pin) == GPIO.LOW and diff < 1:
                diff = time.time() - currentTime
            if (diff * 1000) > 100:
                self.headlight.on()
            else:
                self.headlight.off()

            time.sleep(1)
