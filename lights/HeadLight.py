import RPi.GPIO as GPIO


class HeadLight:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        self.pin = pin
        self.status = 1  # If same harware is used by multiple processes, currently (0: Apis, 1: LDR, 2: Commands)

    def cleanup(self):
        GPIO.cleanup(self.pin)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def toggle(self):
        state = GPIO.input(self.pin)
        if state:
            GPIO.output(self.pin, GPIO.LOW)
        else:
            GPIO.output(self.pin, GPIO.HIGH)
