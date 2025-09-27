import time
from RPi import GPIO


class TubeLight:
    def __init__(self, pin, state):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.state = state
        saved = self.state.load_state().get("tubelight", False)
        self.is_on = bool(saved)
        GPIO.output(pin, GPIO.HIGH if self.is_on else GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup(self.pin)

    def on(self):
        self.is_on = True
        GPIO.output(self.pin, GPIO.HIGH)
        self.state.update_state("tubelight", True)

    def off(self):
        self.is_on = False
        GPIO.output(self.pin, GPIO.LOW)
        self.state.update_state("tubelight", False)

    def toggle(self):
        self.is_on = not self.is_on
        GPIO.output(self.pin, GPIO.HIGH if self.is_on else GPIO.LOW)
        self.state.update_state("tubelight", self.is_on)

    def fun(self):
        for i in range(3):
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(0.3)
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(0.3)
