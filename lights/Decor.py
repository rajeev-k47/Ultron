import RPi.GPIO as GPIO
import time
import random
import threading


class Decor:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        self.pin = pin
        self._running = False
        self._thread = None

    def cleanup(self):
        self.stop()
        GPIO.cleanup(self.pin)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def stop(self):
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join()

    def _run_pattern(self, func, *args):
        self.stop()
        self._running = True
        self._thread = threading.Thread(target=func, args=args, daemon=True)
        self._thread.start()

    def setmode(self, mode, interval=0.5):
        if mode == 0:
            self._run_pattern(self._blink, interval)
        elif mode == 1:
            self._run_pattern(self._fast_blink)
        elif mode == 2:
            self._run_pattern(self._fade_effect)
        elif mode == 3:
            self._run_pattern(self._random_blink)
        else:
            self.stop()

    def _blink(self, interval):
        while self._running:
            self.on()
            time.sleep(interval)
            self.off()
            time.sleep(interval)

    def _fast_blink(self):
        while self._running:
            self.on()
            time.sleep(0.1)
            self.off()
            time.sleep(0.1)

    def _fade_effect(self):
        pwm = GPIO.PWM(self.pin, 100)
        pwm.start(0)
        try:
            while self._running:
                for duty_cycle in range(0, 101, 5):
                    if not self._running:
                        break
                    pwm.ChangeDutyCycle(duty_cycle)
                    time.sleep(0.05)
                for duty_cycle in range(100, -1, -5):
                    if not self._running:
                        break
                    pwm.ChangeDutyCycle(duty_cycle)
                    time.sleep(0.05)
        finally:
            pwm.stop()

    def _random_blink(self):
        while self._running:
            self.on()
            time.sleep(random.uniform(0.05, 0.5))
            self.off()
            time.sleep(random.uniform(0.05, 0.5))

