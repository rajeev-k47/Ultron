import time
from RPi import GPIO


class TubeLight:
    def __init__(self, pin, state):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        self.state = state
        if not self.state.load_state().get("tubelight", 0):
            GPIO.output(pin, GPIO.HIGH)

    def cleanup(self):
        GPIO.cleanup(self.pin)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def toggle(self):
        state = GPIO.input(self.pin)
        self.state.update_state("tubelight", state)
        if state:
            GPIO.output(self.pin, GPIO.LOW)
        else:
            GPIO.output(self.pin, GPIO.HIGH)

    def fun(self):
        for i in range(0, 3):
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(0.3)
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(0.3)
